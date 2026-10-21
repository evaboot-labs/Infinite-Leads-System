# Send leads through n8n

[`n8n/infinite-leads-to-lemlist.n8n.json`](https://raw.githubusercontent.com/evaboot-labs/infinite-leads-system/main/n8n/infinite-leads-to-lemlist.n8n.json)
does the same as the Make scenario, as an n8n workflow for one lead signal. Leads lemlist already
has, or has unsubscribed, are skipped. If lemlist refuses a lead for any other reason, the execution
fails with lemlist's reason, so you see it under **Executions** and can add that lead by hand.

1. Make one copy per signal with a secret webhook path: `python3 n8n/new_workflow.py "Changed jobs"`
   writes `n8n/infinite-leads-changed-jobs.n8n.json` (git ignores it). Anyone who knows a webhook's
   URL can add leads to your campaign, and Evaboot cannot send a secret header, so the random path is
   the lock. No Python? Import the link above and replace the path in **New leads from Evaboot** with a
   long random string yourself.
2. In n8n, create a workflow, open the **⋯** menu and choose **Import from File** with that copy.
3. Open **Your settings** and paste the lemlist campaign id (the `cam_...` part of the campaign's URL).
4. Open **Add the lead to the campaign** and connect your lemlist account with your lemlist API key.
5. Open **New leads from Evaboot**, copy the **Production URL** and give it to your agent: it connects
   that URL to the recurring export for this signal. Then activate the workflow.

The workflow targets lemlist. For any other outreach tool, swap the **Add the lead to the campaign** node for that tool's node in n8n.

Back to the [README](../README.md).
