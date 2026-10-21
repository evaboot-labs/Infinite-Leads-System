"""Build the Make blueprint. Run: python3 make/build_blueprint.py
Writes make/infinite-leads-to-lemlist.blueprint.json (the public template).
With --test OUT CAMPAIGN_ID it writes a filled copy to OUT, reading the key from LEMLIST_API_KEY.

The scenario receives every run of one recurring Evaboot export on a Make webhook and adds each lead
with an email to one lemlist campaign. Evaboot sends one request per run, with the leads in `prospects`.
"""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).parent
LEAD = 3
LEMLIST_FIELDS = [("firstName", "First Name"), ("lastName", "Last Name"), ("jobTitle", "Current Job"),
                  ("companyName", "Company Name"), ("companyDomain", "Company Domain"),
                  ("linkedinUrl", "Linkedin URL Public")]


def field(name):
    # Evaboot names lead fields after the CSV headers, so most of them hold spaces.
    return "{{%d.`%s`}}" % (LEAD, name) if " " in name else "{{%d.%s}}" % (LEAD, name)


def blueprint(api_key, campaign_id):
    flow = [
        {"id": 1, "module": "gateway:CustomWebHook", "version": 1, "parameters": {"hook": None, "maxResults": 1},
         "mapper": {}, "metadata": {"designer": {"x": 0, "y": 0, "name": "New leads from Evaboot"}}},
        {"id": 2, "module": "util:SetVariables", "version": 1, "parameters": {},
         "mapper": {"scope": "roundtrip", "variables": [
             {"name": "lemlist_api_key", "value": api_key},
             {"name": "lemlist_campaign_id", "value": campaign_id}]},
         "metadata": {"designer": {"x": 300, "y": 0, "name": "Your settings"}}},
        {"id": LEAD, "module": "builtin:BasicFeeder", "version": 1, "parameters": {},
         "mapper": {"array": "{{1.prospects}}"},
         "metadata": {"designer": {"x": 600, "y": 0, "name": "One lead at a time"}}},
        # Evaboot leaves Email blank unless the address is deliverable, so a blank one is skipped, not sent.
        # A form body keeps quotes and commas in names intact, which a hand-written JSON body would break on.
        {"id": 4, "module": "http:ActionSendData", "version": 3,
         "parameters": {"handleErrors": True, "useNewZLibDeCompress": True},
         "filter": {"name": "Leads with an email", "conditions": [[{"a": field("Email"), "o": "exist"}]]},
         "mapper": {"url": "https://api.lemlist.com/api/campaigns/{{2.lemlist_campaign_id}}/leads/{{encodeURL(%s)}}" % field("Email")[2:-2],
                    "serializeUrl": False, "method": "post", "headers": [],
                    "qs": [{"name": "deduplicate", "value": "true"}],
                    "bodyType": "x_www_form_urlencoded", "parseResponse": False,
                    "authUser": "", "authPass": "{{2.lemlist_api_key}}",
                    "timeout": "", "shareCookies": False, "ca": "", "rejectUnauthorized": True,
                    "followRedirect": True, "useQuerystring": False, "gzip": True, "useMtls": False,
                    "formFields": [{"key": key, "value": field(name)} for key, name in LEMLIST_FIELDS],
                    "followAllRedirects": False},
         "metadata": {"designer": {"x": 900, "y": 0, "name": "Add the lead to the campaign"}},
         # lemlist answers 400 for a lead it already holds or one in its unsubscribed "graveyard": skip those.
         # Any other error is left unhandled, so Make keeps the run as an incomplete execution to retry,
         # because Evaboot never sends the same batch twice.
         "onerror": [
             {"id": 5, "module": "builtin:Ignore", "version": 1, "parameters": {}, "mapper": None,
              "filter": {"name": "Already in lemlist or unsubscribed", "conditions": [
                  [{"a": "{{4.error.detail}}", "b": "already", "o": "text:contain:ci"}],
                  [{"a": "{{4.error.detail}}", "b": "graveyard", "o": "text:contain:ci"}]]},
              "metadata": {"designer": {"x": 1200, "y": 150, "name": "Skip leads lemlist already has"}}}]},
    ]
    return {"name": "Infinite Leads: new leads to a lemlist campaign", "flow": flow,
            "metadata": {"instant": True, "version": 1,
                         "scenario": {"roundtrips": 1, "maxErrors": 3, "autoCommit": True, "sequential": False,
                                      "confidential": False, "dataloss": False, "dlq": True},
                         "designer": {"orphans": []}}}


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        out, campaign_id = sys.argv[2:4]
        Path(out).write_text(json.dumps(blueprint(os.environ["LEMLIST_API_KEY"], campaign_id)))
        print(f"Wrote {out}")
    else:
        out = HERE / "infinite-leads-to-lemlist.blueprint.json"
        out.write_text(json.dumps(blueprint("YOUR_LEMLIST_API_KEY", "YOUR_LEMLIST_CAMPAIGN_ID"), indent=2) + "\n")
        print(f"Wrote {out}")
