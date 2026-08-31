# ChatGPT Handoff — Image Editing Rules and Skills

Date: 2026-08-31
Source: ChatGPT conversation with Riley
Purpose: Promote durable image-editing routing rules and proposed reusable skills into RileyContext.

## Durable image-editing rules

1. Treat wording such as **exact**, **identical**, **do not change**, **preserve original**, **leave everything else alone**, and equivalent language as a **pixel-locking constraint**, not merely a style preference.
2. For any image with a **single person or character**, facial pixels are locked unless Riley explicitly requests a face change.
3. For any image with a **single person or character**, body size, proportions, and pose are locked unless Riley explicitly requests body or clothing changes.
4. Prefer **deterministic / non-generative editing** whenever the requested result can be achieved without synthesizing new subject pixels. Examples: background removal, transparent backgrounds, cutouts, crop/resize, compositing existing assets, borders/outlines/sticker edges, canvas changes, transparency, and ordinary color/exposure/brightness adjustments.
5. When exact preservation is required, choose an available specialized connected app/tool/plugin or deterministic image-processing workflow before generative image editing. Riley should not need to know or type the `@` app name for correct routing.
6. Use generative editing only when the request actually requires new visual content, such as a new outfit, hairstyle, pose, body change, scene/background content, added/removed objects, or a new image. Preserve all non-requested regions as tightly as the available tool permits.
7. If the requested change requires generative synthesis and exact preservation of affected pixels cannot be guaranteed, state that limitation before performing the edit and choose the route with the strongest preservation controls available.
8. If Riley says an edit drifted or changed something that was supposed to stay exact, do **not** keep retrying the same generative workflow. Reclassify the task and switch to a deterministic/specialized tool route when available.
9. Preferred exact sticker workflow: preserve original foreground pixels → derive alpha/subject mask → expand/dilate the mask for requested border width → render border behind untouched foreground.
10. App/tool routing: `@` mentions are optional. Automatically use connected apps/tools when intent is clear; use explicit `@` selection only when Riley specifically wants a particular app/destination or when multiple valid routes exist and the chosen app matters.
11. Search and Deep Research are capabilities/modes used within Chat, not GPT models. Use Search for current quick lookup, Deep Research for exhaustive multi-source investigation, Work for multi-step execution, and Codex for coding/repository work.

## Proposed reusable skills

Create a minimal three-skill image-editing system rather than many narrow skills:

### 1. image-edit-routing
Entry point for every existing-image edit.
- Identify requested change.
- Identify locked regions/pixels before selecting a tool.
- Classify task as deterministic, generative, or mixed.
- Prefer deterministic/specialized connected-tool routes for exact-preservation tasks.
- Do not repeat a generative route after user-reported drift when a deterministic route exists.

### 2. exact-image-edit
For pixel-preserving transformations.
- Background removal / transparency / cutouts
- Crop / resize / canvas changes
- Existing-asset compositing
- Sticker borders / outlines / edge cleanup
- Traditional color, exposure, and brightness adjustments
- Success criterion: unchanged pixels remain unchanged.

### 3. identity-preserving-generative-edit
For edits that require synthesis around a person/character.
- Clothing changes
- Hair changes
- Pose/body changes
- New scenes/background content
- Added/removed scene elements
- Explicit requested-region vs locked-region handling
- Locked face/body defaults unless specifically overridden by Riley
- Warn before execution when the affected area cannot be preserved exactly.

## Regression tests

1. **Background removal:** User uploads a single-person image and says “remove the background; do not change me.” Expected: non-generative/specialized background-removal route; face/body untouched.
2. **Sticker edit:** User says “make this a transparent sticker with a thin white outline; leave the character identical.” Expected: deterministic mask/outline workflow; no subject regeneration.
3. **Clothing edit:** User says “put me in this jacket; do not change my face, body size, proportions, or pose.” Expected: generative clothing edit with face/body locks and explicit preservation constraint.
4. **Drift recovery:** User says “you changed my face again.” Expected: stop repeating same generative route, reclassify task, choose a stronger identity-preserving or deterministic workflow if possible.

## Promotion intent

This handoff is intentionally durable and should be incorporated into the RileyContext operating rules and/or authoritative skills system so all compatible models and agents inherit the same image-editing behavior.
