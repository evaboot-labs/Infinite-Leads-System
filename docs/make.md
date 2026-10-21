# Send leads through Make

[`make/infinite-leads-to-lemlist.blueprint.json`](https://raw.githubusercontent.com/evaboot-labs/infinite-leads-system/main/make/infinite-leads-to-lemlist.blueprint.json)
is a Make scenario for one lead signal. Evaboot sends each run of the recurring export to the
scenario's webhook, and the scenario adds every lead with an email to your lemlist campaign. Leads
already in the campaign, or unsubscribed in lemlist, are skipped. If lemlist refuses a lead for any
other reason, Make keeps it under **Incomplete executions** so you can retry it: Evaboot never sends
the same batch twice. Use it when you want to filter, enrich or route leads in Make
before they reach the campaign; otherwise Evaboot's own lemlist and Instantly integrations do the
same job with nothing to host.

1. In Make, create a scenario, open the **⋮** menu and choose **Import blueprint**, then pick the
   file (or download it from the link above first).
2. Click **New leads from Evaboot**, then **Add** to create a webhook, and copy its URL.
   Give that URL to your agent: it connects it to the recurring export for this signal.
3. Open **Your settings** and fill in your lemlist API key (lemlist, **Settings**, **Integrations**)
   and the campaign id (the `cam_...` part of the campaign's URL in lemlist).
4. Switch the scenario on. It runs each time Evaboot sends a batch.
5. Import it once per signal, so each signal keeps its own campaign. Make's free plan runs two
   active scenarios.

`make/build_blueprint.py` writes the blueprint; `--test` fills in real values for a test run.

The blueprint targets lemlist. For any other outreach tool, swap the **Add the lead to the campaign** module for that tool's module in Make.

Back to the [README](../README.md).
