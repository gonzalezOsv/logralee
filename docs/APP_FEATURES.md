# Logralee — everything the app has

> Source of truth for the website's claims. Built from the iOS repo (`~/Dev/logralee-ios`) on **2026-10-13**.
> iOS is the lead platform; Android is porting the same features and copy and is expected to catch up by late October 2026.
> Re-check every number here against the code before launch. If it isn't in this file, the site doesn't claim it.

**Status key:** ✅ ships at launch · 🚩 built, hidden behind a flag for launch · 🛠 in progress · 🗺 roadmap (not before launch)

---

## 1. The idea in one line

A journal for every way you move. Log any kind of training in seconds, keep the story, and get celebrated for showing up. Judgment-free: no guilt, no streak pressure, rest days are part of the plan, plain words instead of gym jargon.

**Name:** *lograr* (Spanish, "to achieve") + *log*.

---

## 2. Platform basics

| | Status | Notes |
|---|---|---|
| iPhone app (iOS 26+, native SwiftUI, Liquid Glass) | ✅ | Lead platform |
| Android app (native Kotlin / Jetpack Compose, Material 3) | 🛠 | Porting from iOS; same behavior and copy |
| Tabs | ✅ | Home · Log · Journal · Routines · Profile |
| Offline-first, data stored on the phone | ✅ | SwiftData on device. Works in airplane mode |
| Account / sign-in | ❓ | Login + Register screens exist and run in Release builds. **Confirm whether an account is required at launch** before the site says "no account needed" |
| Cloud sync | 🗺 | Not at launch. Don't name a provider on the site |

---

## 3. Logging

| Feature | Status | Notes |
|---|---|---|
| Log any activity | ✅ | Activity chips: Strength, Cardio, CrossFit, Yoga, Mobility — each with a sub-sort (e.g. Strength → Chest, Back) |
| Entry types | ✅ | Strength sets, cardio, timed holds, bodyweight |
| Exercise library | ✅ | **251 exercises**, **45 muscles** mapped (`catalog/exercises.json`, `catalog/muscles.json`) |
| Custom exercises | ✅ | Create your own |
| Rest timer | ✅ | Ring countdown, −30 / +30 / Skip; starts when you log |
| Weight units | ✅ | lb / kg preference |
| Activity icons | ✅ | Eight brush-stroke icons in the logo's style: strength, run, ride, row, CrossFit, yoga, mobility, bodyweight |

## 4. Routines and plans

| Feature | Status | Notes |
|---|---|---|
| Ready-made routines | ✅ | **110** in `catalog/routines` — strength plus CrossFit-style WODs (weightlifting, gymnastics, monostructural), yoga (mind-body) and mobility |
| Plans | ✅ | **26** multi-week plans, e.g. Kickstart, Starter Strength, Push Pull Legs, Upper Lower, Texas Method, Smolov Jr., German Volume Training, 20-Rep Squat, First Month on the Mat, Hips and Hamstrings, Ten Minutes a Day, Garage Minimal, Legs First, Engine Builder |
| Plan pages | ✅ | Tabbed About card: the pitch, what the plan covers, how it fits your week, how to progress. Weeks collapsed, with a progress bar |
| Build your own routine | ✅ / 🛠 | Editor exists; per-activity rework (any routine type: strength, yoga, cardio, CrossFit, mixes) in progress |
| Up next pairing | ✅ | Pair two routines (yours or ready-made); finish one and the next is ready. "Build your own" row in the picker is 🚩 until the editor rework lands |
| Active workout screen | ✅ | Check to log a set (one way to log), easy exercise switching, floating advance pill (next / finish), minimize bar so other tabs stay reachable, end any time |
| Guided flows | ✅ | Yoga and mobility run as a guided session player (pose, timer, progress) |
| Session summary | ✅ | End-of-workout recap |
| AI routine generation | 🚩 | Engine built and tested; entry points hidden for launch |
| Copy a class from a whiteboard photo | 🗺 | Needs image-to-text |

## 5. Coaching engine

| Feature | Status | Notes |
|---|---|---|
| Three levels | ✅ | Off · Minimal · Full |
| Warm-up sets | ✅ | Generated warm-ups before working sets (`WarmupSetGenerator`) |
| Session intent and goals | ✅ | Each session gets an intent ("dial-in") and targets (`SessionIntentResolver`, `SessionGoalResolver`, `CoachingTargetEngine`) |
| Live cues | ✅ | Plain-language cues per exercise (`CueResolver`, `CoachBrief`) |
| Readiness and deload safety | ✅ | Readiness ceiling, deload set clamp, effort-drift signals |
| Smart swaps | ✅ | Ranked alternatives when equipment is busy (`SwapExerciseRanker`) |
| Finish summary | ✅ | Coach's wrap-up at the end of a session |
| Dynamic coaching box | 🛠 | One box that appears only when relevant (logged more/fewer reps, rest needs) |
| Volume governor | ❌ | Not built |

Voice rules: no RPE/RIR/1RM acronyms in user copy; derived numbers ("estimated max") in plain words; no guilt framing.

## 6. 3D movement guides

| Feature | Status | Notes |
|---|---|---|
| How-to player | ✅ (confirm) | 3D figure performs the movement. Opens from Exercise detail and the routine editor |
| Coverage | 🛠 | **80 of 185** movements used in shipped routines have motions: yoga/mobility 54 of 56, strength 24 of 112, conditioning 2 of 6, cardio 0 of 11 (`catalog/motions/COVERAGE.md`) |
| Your Figure | ✅ | Pick the figure in Profile |
| Muscle highlighting on the figure | 🛠 | Anatomical muscle shapes that light up |
| Figure inside the yoga player | 🛠 | Work order written; animated hide/show |

## 7. Journal

| Feature | Status | Notes |
|---|---|---|
| Day cards | ✅ | Weekday + date as the title, body-part badge, camera icon when a Moment exists |
| Rest gaps and month separators | ✅ | Gaps shown kindly, never shamed |
| Year view | ✅ | 12 mini months ("year wall") |
| Session detail and editing | ✅ | |

## 8. Moments

| Feature | Status | Notes |
|---|---|---|
| Capture | ✅ | In-app camera, selfies mirrored like Snapchat, fast shutter |
| Editor | ✅ | Three tools at the bottom: Workout, Look, Filter. Layout carousel, card starts centered, move it anywhere |
| Whole-day cards | ✅ | Everything logged that day across activities (lifting, CrossFit, yoga…) |
| PR celebration | ✅ | PR chip only when earned; sparkles/confetti. First-ever log is celebrated but isn't a PR. No streaks on cards |
| Save sheet | ✅ | One Save button → Overlay (transparent PNG, Strava-style), Stories, Share |
| Photo filters | 🛠 | Photographic-style "looks" |
| Gallery | ✅ | All your Moments |
| On This Day / Then vs Now | ✅ | Resurfaces past Moments |

Positioning: Logralee's answer to Strava's photo-with-stats share, for lifting and every other activity. Saving comes first; sharing is optional.

## 9. Progress and insights

| Feature | Status | Notes |
|---|---|---|
| My Progress | ✅ | "Distance travelled": one headline number for weight added since a date, then each lift start → now. Pin your lifts; auto-fills from most-logged |
| Insights | ✅ / 🛠 | Muscle-region detail, week detail, past recaps. Insights v2 redesign planned |
| Exercise detail | ✅ | Per-lift chart and history |
| Premium | 🗺 | "Coming soon" sheet: deeper insights, a higher tracked-lift limit, coach-managed plans later. "Nothing you use today gets taken away." Everything is included at launch |

## 10. Weight

| Feature | Status | Notes |
|---|---|---|
| Weight screen | ✅ | Scale-tape hero, stat tiles, Today card with log button, trend chart, weekly-average bars, recent weigh-ins |
| Goal or no goal | ✅ | Set/edit a goal in a small sheet, or "just logging my weight" mode |

## 11. Home

| Feature | Status | Notes |
|---|---|---|
| Greeting + week calendar | ✅ | |
| Today | ✅ | Cover Flow of today's routines/plans with activity pill |
| Moments card | ✅ | Latest Moment blurred as the background, big shutter button |
| New-user Home | ✅ | Ad-style carousel personalized from onboarding (plans, logging, routines, yoga, cardio, CrossFit) |

## 12. Lock Screen

| Feature | Status | Notes |
|---|---|---|
| Live Activity | ✅ | Lift name, reps × weight, set number. Three controls; log without unlocking |

## 13. Make it yours

| Feature | Status | Notes |
|---|---|---|
| Themes | ✅ | **7**: Cotton Candy (default), Rose, Lavender, Forest, Terracotta, Sand, Slate — each light and dark |
| Onboarding | ✅ | Terms → about you → interests → goal → level → theme. Questions skippable after terms/name |
| Notifications | 🗺 | Settings screen says "coming soon" |

## 14. Privacy

| Feature | Status | Notes |
|---|---|---|
| Data on device | ✅ | Training data stored locally |
| Cycle tracking | 🚩 | Built (own backup-excluded store, never syncs) but hidden for launch; planned as a post-launch wellness rebuild. **Site must not mention it** |

## 15. Roadmap (not for launch claims)

- Year in Review (Wrapped-style shareable stat cards), as an update in 2027
- Copy a class from a whiteboard photo
- Premium tier
- Cloud sync and accounts across devices
- AI routine generation (built, hidden)
- Cycle-aware wellness (rebuild)

---

## Website claim checklist

| Claim | OK to use? |
|---|---|
| "Coming this December to iPhone and Android" | Owner's target. Confirm before going live |
| 110 routines · 26 plans · 251 exercises · 45 muscles | ✅ verified 2026-10-13 |
| Seven themes, light and dark | ✅ |
| Works offline, data on your phone | ✅ |
| "No account needed to start" | ❓ confirm (see §2) |
| 3D guides | ✅ if How-to ships; say "a growing library", not a number, until coverage is higher |
| Free to download, free features stay free | ✅ matches the Premium sheet |
| Anything about cycle tracking, AI plans, cloud sync, Cloudflare | ❌ don't claim |
