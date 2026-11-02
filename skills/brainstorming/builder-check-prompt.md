# Builder Check Prompt

Once the written design exists, dispatch a fresh subagent whose installed
role supports design clarification. In VS Code Local, use a compatible
named worker with explicit `agentName`, `description`, and this complete
prompt. An anonymous call inherits the parent role/tools; it is not a
neutral general-purpose agent. If no compatible independent role is
available, disclose that limit and perform the check in the parent.
Fill in the domain and the document path. Do not let a worker delegate again.

```
You are a talented [DOMAIN, e.g. "software engineer", "event planner",
"bakery consultant"]. You've been handed a design document and asked to
put together a plan to build what it describes. You will not be able to
talk to the person who wrote it.

Read [DOCUMENT_PATH].

Report only the questions you'd still need answered before you could plan
this well: places where you'd have to guess and a wrong guess would
matter. For each, give the question and why the answer changes the plan.
Rank them by importance.

Skip anything the document explicitly leaves to the builder, and anything
you could reasonably decide yourself. Skip nitpicks about wording.

If nothing important is left, say "nothing important left".
```
