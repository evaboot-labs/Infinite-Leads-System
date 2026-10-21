"""Write one signal's copy of the n8n workflow with a secret webhook path.

Run: python3 n8n/new_workflow.py "Changed jobs" [CAMPAIGN_ID]
Writes n8n/unlimited-leads-<signal>.n8n.json to import into n8n. Anyone who knows a webhook's URL can
post leads into the campaign, and Evaboot cannot send a secret header, so the path itself is the secret.
"""
import json
import re
import secrets
import sys
from pathlib import Path

HERE = Path(__file__).parent


def main():
    if len(sys.argv) < 2:
        sys.exit('Usage: python3 n8n/new_workflow.py "<signal name>" [lemlist campaign id]')
    signal = sys.argv[1]
    workflow = json.loads((HERE / "unlimited-leads-to-lemlist.n8n.json").read_text())
    workflow["name"] = f"Unlimited Leads · {signal}"
    for node in workflow["nodes"]:
        if node["type"] == "n8n-nodes-base.webhook":
            node["parameters"]["path"] = "unlimited-leads-" + secrets.token_urlsafe(24)
            node.pop("webhookId", None)
        if node["name"] == "Your settings" and len(sys.argv) > 2:
            node["parameters"]["assignments"]["assignments"][0]["value"] = sys.argv[2]
    slug = re.sub(r"[^a-z0-9]+", "-", signal.lower()).strip("-")
    out = HERE / f"unlimited-leads-{slug}.n8n.json"
    out.write_text(json.dumps(workflow, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {out}. Import it in n8n with Import from File; the webhook path is secret, keep the file out of git.")


if __name__ == "__main__":
    main()
