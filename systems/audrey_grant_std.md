### Audrey Grant Modern Standard System Definition File

This document defines the logical parameters for the **Audrey Grant Modern Standard** system (also known as Grant Standard), based on the provided technical excerpts and logic schemas. It includes both Basic (Standard) and Advanced conventions.

---

### 1. Hand Evaluation

**High Card Point (HCP) Ranges**
The system classifies hands into three primary strength tiers to determine rebid logic:
* **Minimum:** 12–15 points.
* **Medium:** 16–18 points.
* **Maximum:** 19–21 points.

**Distributional Points**
Points are added to HCP based on the role in the auction:
* **Length Points (Used by Opener):** Applied when deciding to open. Add **1 point** for a 5-card suit, **2 points** for a 6-card suit, and **3 points** for a 7-card suit.
* **Dummy/Shortness Points (Used by Responder):** Applied **only after a fit (3+ cards)** is found in partner’s major suit. 
    * **Void:** 5 points.
    * **Singleton:** 3 points.
    * **Doubleton:** 1 point.

**Specific Evaluation Rules**
* **Rule of 20:** A hand in 1st or 2nd seat may be opened if the **HCP + the length of the two longest suits equals 20 or more**.
* **Balanced Hand Definition:** A hand is balanced if it contains **no singleton, no void, and a maximum of one doubleton**.

---

### 2. Opening Bids

**No-Trump Openings (Balanced Hands)**
* **1NT:** 15–17 HCP.
* **2NT:** 20–21 HCP.
* **3NT:** 25–27 HCP.
* *Note:* Balanced hands with 12–14 HCP open a suit and rebid 1NT; 18–19 HCP open a suit and jump in 2NT.

**Priority of Suits**
1.  **5-Card Majors:** Open 1H or 1S with 12–21 total points and 5+ cards. If 5-5 in majors, open the **higher-ranking suit (Spades)**.
2.  **Best Minor:** Open 1C or 1D if the hand does not meet Major or NT criteria. 
    * If **4-4 in minors**, open **1 Diamond**.
    * If **3-3 in minors**, open **1 Club**.
    * If unequal length, open the **longer minor**.

**2-Level and Preemptive Openings**
* **2 Clubs (Strong/Artificial):** 22+ total points or 9+ tricks if unbalanced; forcing to at least 2NT or a suit agreement.
* **Weak Two-Bids (2D, 2H, 2S):** 5–11 HCP (or 5–10) with a **good 6-card suit** usually containing 2 of the top 3 honors.
* **Preempts (3-level/4-level):** Weak hand with a **7-card suit** (3rd level) or **8-card suit** (4th level).

---

### 3. Responder's Logic

**Responses to 1 Major (e.g., 1 Heart)**
* **Support (Fit Found):** 2H (6–10 dummy points), 3H (11–12 points, Invitational/Limit), 4H (13+ points, Game Force).
* **Jacoby 2NT:** 13+ dummy points and **4+ card support**; forcing to game. (Treat as *Advanced* if checking complexity).
* **Splinter Raises:** Double jump in a new suit shows 4+ support, game strength, and a **singleton or void** in the bid suit. (Treat as *Advanced*).
* **New Suit:** 1S over 1H requires 6+ HCP and 4+ cards (Forcing). A 2-level minor response requires 10+ (Basics) or 12+ (Standard/Game Force) HCP and usually 5+ cards.
* **1NT Response:** 6–9 HCP; denies support and denies a 1-level suit bid (the "dustbin" bid).

**Responses to 1NT (15–17 HCP)**
* **Stayman (2C):** 8+ HCP with at least one **4-card major**.
* **Jacoby Transfers (2D/2H):** 0+ points with 5+ cards in the major; 2D transfers to Hearts, 2H transfers to Spades.
* **Extended Transfers (2S):** Transfer to **3 Clubs** to sign off in a minor.
* **Invitational:** 2NT (8–9 HCP).

**Responses to 2 Clubs**
* **2 Diamonds:** The "waiting" bid.
* **Second Negative:** The cheaper of 3C/3D shows a weak hand after an initial 2D response.

---

### 4. Rebids & Slam Zone

**Opener’s Rebids (After 1-over-1 Response)**
* **Priority 1 (Support):** Raise with 4-card support. Raise to 2 (Minimum), 3 (Medium), or 4 (Maximum).
* **Priority 2 (NT):** 1NT (12–14 balanced), 2NT (18–19 balanced jump).
* **Priority 3 (New Suit):** Lower rank is non-forcing; **Reverse bid** (higher rank than first suit) requires **17+ HCP**.
* **Priority 4 (Rebid First Suit):** Requires 6+ cards. Level indicates strength (Min=2-level, Med=3-level).

**Opener’s Rebids (After 1NT Response)**
* **Pass:** 12–14 HCP and balanced.
* **2 of New Suit:** Unbalanced hand; requires the second suit to be lower ranking than the first.

**Slam Conventions**
* **Gerber (4C):** Used to ask for Aces only after a **natural 1NT or 2NT** bid.
* **Blackwood (4NT):** Used to ask for Aces after a **suit is agreed**.
* **Fourth Suit Forcing:** Use of the fourth suit as an artificial bid to create a **game-forcing** situation.

---

### 5. Competitive Bidding

**Overcalls and Interference**
* **1NT Overcall:** 15–18 HCP with a stopper.
* **Weak Two/Preemptive Overcalls:** Use same suit length/quality requirements as opening preempts.
* **Interference Over 1NT Opening:**
    * If doubled: Stayman and Transfers remain on.
    * If 2C overcall: **Double is Stayman**; Transfers remain on.
    * If 2D or higher: Transfers are **off**; a cuebid of the opponent's suit is Stayman.

**Takeout Doubles and Negative Doubles**
* **Negative Doubles:** Used in competition through the level of 3S to show unbid suits.
* **Takeout Double:** Shows opening values and support for unbid suits.

---

### 6. Advanced / Competitive Extensions (Advanced Mode)

**Slam Investigation**
* **Control Bidding (Cue Bidding):**
    * Used after a major suit is agreed and the auction is forcing to game.
    * A bid of a new suit at the 3-level or 4-level (below game) shows a **Control** (Ace or King) in that suit.
    * **Priority:** Show **First Round Controls** (Aces/Voids) before **Second Round Controls** (Kings/Singletons).
    * *Constraint:* Do not use Blackwood if you have two quick losers in an unbid suit; use Control Bids instead.

**Refined Conventions**
* **Roman Keycard Blackwood (RKC 1430):**
    * Replaces Standard Blackwood in Advanced contexts.
    * The "Five Aces" are the 4 Aces + the King of Trumps.
    * **Responses to 4NT:**
        * 5C: 1 or 4 Keycards.
        * 5D: 0 or 3 Keycards.
        * 5H: 2 Keycards (without Queen of Trumps).
        * 5S: 2 Keycards (with Queen of Trumps).

**Competitive Adjustments**
* **Lebensohl (Advanced):**
    * Used after an opponent interferes with a 1NT opening (e.g., 1NT - (2H) - ?).
    * **2NT** is artificial and forces Opener to bid **3C**. Responder can then Pass (to play 3C) or sign off in a suit lower than the opponent's suit.
    * Direct bids at the 3-level are forcing.