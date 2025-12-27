import os

# The clean, master copy of the system so far
YAML_CONTENT = """Dealer:
  - bid: "Pass"
    type: "Opening"
    convention: "Natural"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "0-11 HCP (or 12 w/o opening shape)."
    explanation: "We lack the strength to open. We do not meet the Rule of 20."
    hint_on_miss: "Count your points. If you have fewer than 12 HCP and don't meet the Rule of 20, Pass."
    constraints:
      max_hcp: 12
      rule_of_20: false
      evaluation_method: "HCP"

  - bid: "1C"
    type: "Opening"
    convention: "Better Minor"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "12-21 Total Points, 3+ Clubs."
    explanation: "With no 5-card major and strictly less than 3 Diamonds (meaning 3-3 in minors) or longer Clubs than Diamonds."
    hint_on_miss: "If you have no 5-card major and your minors are equal length (3-3), open 1C."
    constraints:
      min_hcp: 12
      max_hcp: 21
      shape_requirements: "3+ Clubs, No 5-card Major"
      priority: "Lowest"
      evaluation_method: "Length Points"

  - bid: "1D"
    type: "Opening"
    convention: "Better Minor"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "12-21 Total Points, 3+ Diamonds (usually 4+)."
    explanation: "With no 5-card major, we open our longer minor. With 4-4 or 3-3 in Diamonds/Clubs, we prefer 1D."
    hint_on_miss: "If you have equal length minors (4-4), open 1D."
    constraints:
      min_hcp: 12
      max_hcp: 21
      shape_requirements: "3+ Diamonds, No 5-card Major"
      evaluation_method: "Length Points"

  - bid: "1H"
    type: "Opening"
    convention: "5-Card Major"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "12-21 Total Points, 5+ Hearts."
    explanation: "We have opening values and a 5-card Major. This is our first priority."
    hint_on_miss: "Always open a 5-card Major if you have the points (Priority #1)."
    constraints:
      min_hcp: 12
      max_hcp: 21
      shape_requirements: "5+ Hearts"
      priority: "High"
      evaluation_method: "Length Points"

  - bid: "1S"
    type: "Opening"
    convention: "5-Card Major"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "12-21 Total Points, 5+ Spades."
    explanation: "We have opening values and a 5-card Major. This is our first priority."
    hint_on_miss: "Always open a 5-card Major if you have the points (Priority #1)."
    constraints:
      min_hcp: 12
      max_hcp: 21
      shape_requirements: "5+ Spades"
      priority: "High"
      evaluation_method: "Length Points"

  - bid: "1NT"
    type: "Opening"
    convention: "Natural"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "15-17 HCP, Balanced."
    explanation: "A balanced hand with 15-17 HCP. This limits our hand immediately."
    hint_on_miss: "With 15-17 HCP and a balanced shape, open 1NT to describe your hand in one bid."
    constraints:
      min_hcp: 15
      max_hcp: 17
      shape_requirements: "Balanced"
      evaluation_method: "HCP"

  - bid: "2C"
    type: "Opening"
    convention: "Strong Artificial"
    complexity: "Basic"
    forcing_status: "Forcing"
    inference: "22+ Total Points."
    explanation: "This hand is too strong for a 1-level opening. 2C forces partner to respond."
    hint_on_miss: "With 22+ points, you must open 2C."
    constraints:
      min_hcp: 22
      evaluation_method: "HCP"

  - bid: "2D"
    type: "Opening"
    convention: "Weak Two"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "5-11 HCP, 6 Good Diamonds."
    explanation: "A preemptive opening showing a good 6-card suit but less than opening strength."
    constraints:
      min_hcp: 5
      max_hcp: 11
      shape_requirements: "6 Diamonds"
      evaluation_method: "HCP"

  - bid: "2H"
    type: "Opening"
    convention: "Weak Two"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "5-11 HCP, 6 Good Hearts."
    explanation: "A preemptive opening showing a good 6-card suit but less than opening strength."
    constraints:
      min_hcp: 5
      max_hcp: 11
      shape_requirements: "6 Hearts"
      evaluation_method: "HCP"

  - bid: "2S"
    type: "Opening"
    convention: "Weak Two"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "5-11 HCP, 6 Good Spades."
    explanation: "A preemptive opening showing a good 6-card suit but less than opening strength."
    constraints:
      min_hcp: 5
      max_hcp: 11
      shape_requirements: "6 Spades"
      evaluation_method: "HCP"

  - bid: "2NT"
    type: "Opening"
    convention: "Natural"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "20-21 HCP, Balanced."
    explanation: "A specific opening for balanced hands with 20-21 HCP."
    constraints:
      min_hcp: 20
      max_hcp: 21
      shape_requirements: "Balanced"
      evaluation_method: "HCP"

  - bid: "3C"
    type: "Opening"
    convention: "Preempt"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "Weak hand, 7+ Clubs."
    constraints:
      max_hcp: 10
      shape_requirements: "7+ Clubs"
      evaluation_method: "HCP"

  - bid: "3D"
    type: "Opening"
    convention: "Preempt"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "Weak hand, 7+ Diamonds."
    constraints:
      max_hcp: 10
      shape_requirements: "7+ Diamonds"
      evaluation_method: "HCP"

  - bid: "3H"
    type: "Opening"
    convention: "Preempt"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "Weak hand, 7+ Hearts."
    constraints:
      max_hcp: 10
      shape_requirements: "7+ Hearts"
      evaluation_method: "HCP"

  - bid: "3S"
    type: "Opening"
    convention: "Preempt"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "Weak hand, 7+ Spades."
    constraints:
      max_hcp: 10
      shape_requirements: "7+ Spades"
      evaluation_method: "HCP"

"1H":
  - bid: "Pass"
    type: "Response"
    convention: "Natural"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "0-5 HCP, usually no fit or too weak to respond."
    explanation: "With fewer than 6 High Card Points, we generally do not have enough strength to keep the auction open."
    hint_on_miss: "You need at least 6 points to respond to a 1-level opening."
    constraints:
      min_hcp: 0
      max_hcp: 5
      shape_requirements: "Any"
      evaluation_method: "HCP"

  - bid: "1S"
    type: "Response"
    convention: "Natural"
    complexity: "Basic"
    forcing_status: "Forcing"
    inference: "6+ HCP, 4+ Spades."
    explanation: "With 6+ points and a 4-card spade suit, showing the major is our top priority."
    hint_on_miss: "Always show a 4-card Spade suit if you have 6+ points."
    constraints:
      min_hcp: 6
      max_hcp: 21
      shape_requirements: "4+ Spades"
      evaluation_method: "HCP"

  - bid: "1NT"
    type: "Response"
    convention: "Natural"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "6-9 HCP, denies 4 Spades, denies 3+ Hearts."
    explanation: "This is the 'dustbin' bid. We have 6-9 points but lack support for partner and do not have 4 Spades to bid 1S."
    hint_on_miss: "Without support or a Spade suit, bid 1NT to show minimum values (6-9)."
    constraints:
      min_hcp: 6
      max_hcp: 9
      shape_requirements: "No 4+ Spades, <3 Hearts"
      evaluation_method: "HCP"

  - bid: "2C"
    type: "Response"
    convention: "Natural"
    complexity: "Basic"
    forcing_status: "Forcing"
    inference: "10+ HCP, 5+ Clubs (rarely 4)."
    explanation: "A new suit at the 2-level requires more strength (10+ points) and usually promises a 5-card suit."
    hint_on_miss: "You need 10+ points to introduce a new suit at the 2-level."
    constraints:
      min_hcp: 10
      max_hcp: 21
      shape_requirements: "5+ Clubs"
      evaluation_method: "HCP"

  - bid: "2D"
    type: "Response"
    convention: "Natural"
    complexity: "Basic"
    forcing_status: "Forcing"
    inference: "10+ HCP, 5+ Diamonds."
    explanation: "A new suit at the 2-level requires more strength (10+ points) and usually promises a 5-card suit."
    hint_on_miss: "You need 10+ points to introduce a new suit at the 2-level."
    constraints:
      min_hcp: 10
      max_hcp: 21
      shape_requirements: "5+ Diamonds"
      evaluation_method: "HCP"

  - bid: "2H"
    type: "Response"
    convention: "Simple Raise"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "6-10 Dummy Points, 3+ Hearts."
    explanation: "A minimum raise shows we have found a fit and have 6-10 points (counting Shortness points)."
    hint_on_miss: "With a fit and minimum values (6-10), raise partner strictly to the 2-level."
    constraints:
      min_dummy_points: 6
      max_dummy_points: 10
      shape_requirements: "3+ Hearts"
      evaluation_method: "Dummy Points"

  - bid: "2NT"
    type: "Response"
    convention: "Jacoby 2NT"
    complexity: "Advanced"
    forcing_status: "Game Forcing"
    inference: "13+ Dummy Points, 4+ Hearts."
    explanation: "An artificial game-forcing raise asking opener to show shortness."
    hint_on_miss: "With game-going values and 4+ trumps, use 2NT (Jacoby) to investigate slam."
    constraints:
      min_dummy_points: 13
      shape_requirements: "4+ Hearts"
      evaluation_method: "Dummy Points"

  - bid: "3H"
    type: "Response"
    convention: "Limit Raise"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "11-12 Dummy Points, 3+ Hearts."
    explanation: "An invitational jump raise showing medium strength and support."
    hint_on_miss: "With 11-12 points and support, jump to 3 to invite partner to Game."
    constraints:
      min_dummy_points: 11
      max_dummy_points: 12
      shape_requirements: "3+ Hearts"
      evaluation_method: "Dummy Points"

  - bid: "3S"
    type: "Response"
    convention: "Splinter"
    complexity: "Advanced"
    forcing_status: "Game Forcing"
    inference: "13+ Points, 4+ Hearts, Singleton/Void in Spades."
    explanation: "A double jump shift showing game values, trump support, and shortness in the bid suit."
    hint_on_miss: "Consider a Splinter bid to show your singleton and game values immediately."
    constraints:
      min_dummy_points: 13
      shape_requirements: "4+ Hearts, Max 1 Spade"
      evaluation_method: "Dummy Points"

  - bid: "4C"
    type: "Response"
    convention: "Splinter"
    complexity: "Advanced"
    forcing_status: "Game Forcing"
    inference: "13+ Points, 4+ Hearts, Singleton/Void in Clubs."
    explanation: "A double jump shift showing game values, trump support, and shortness in the bid suit."
    hint_on_miss: "Consider a Splinter bid to show your singleton and game values immediately."
    constraints:
      min_dummy_points: 13
      shape_requirements: "4+ Hearts, Max 1 Club"
      evaluation_method: "Dummy Points"

  - bid: "4D"
    type: "Response"
    convention: "Splinter"
    complexity: "Advanced"
    forcing_status: "Game Forcing"
    inference: "13+ Points, 4+ Hearts, Singleton/Void in Diamonds."
    explanation: "A double jump shift showing game values, trump support, and shortness in the bid suit."
    hint_on_miss: "Consider a Splinter bid to show your singleton and game values immediately."
    constraints:
      min_dummy_points: 13
      shape_requirements: "4+ Hearts, Max 1 Diamond"
      evaluation_method: "Dummy Points"

  - bid: "4H"
    type: "Response"
    convention: "Game Raise"
    complexity: "Basic"
    forcing_status: "Sign-off"
    inference: "13+ Dummy Points, usually balanced or flat distribution."
    explanation: "A direct jump to game usually denies interest in slam (Fast Arrival) or simply closes the auction."
    hint_on_miss: "If you have game values but no slam interest, go directly to 4H."
    constraints:
      min_dummy_points: 13
      shape_requirements: "3+ Hearts"
      evaluation_method: "Dummy Points"

"1H - 1S":
  - bid: "1NT"
    type: "Rebid"
    convention: "Natural"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "12-14 HCP, Balanced distribution."
    explanation: "With a balanced minimum hand (12-14) and no support for Spades, we rebid 1NT."
    hint_on_miss: "If you are balanced with minimum values and no fit, rebid 1NT."
    constraints:
      min_hcp: 12
      max_hcp: 14
      shape_requirements: "Balanced, <4 Spades"
      evaluation_method: "HCP"

  - bid: "2C"
    type: "Rebid"
    convention: "Natural"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "12-17 HCP, 4+ Clubs."
    explanation: "Bidding a new suit at a lower level is natural and non-forcing. It usually shows 4+ cards in the second suit."
    hint_on_miss: "Show your second suit (Clubs) if you have 4+ cards."
    constraints:
      min_hcp: 12
      max_hcp: 17
      shape_requirements: "5+ Hearts, 4+ Clubs"
      evaluation_method: "Length Points"

  - bid: "2D"
    type: "Rebid"
    convention: "Natural"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "12-17 HCP, 4+ Diamonds."
    explanation: "Bidding a new suit at a lower level is natural and non-forcing. It usually shows 4+ cards in the second suit."
    hint_on_miss: "Show your second suit (Diamonds) if you have 4+ cards."
    constraints:
      min_hcp: 12
      max_hcp: 17
      shape_requirements: "5+ Hearts, 4+ Diamonds"
      evaluation_method: "Length Points"

  - bid: "2H"
    type: "Rebid"
    convention: "Rebid First Suit"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "12-15 Total Points, 6+ Hearts."
    explanation: "With a minimum hand and a long suit (6+), rebid your major to show extra length."
    hint_on_miss: "Do not rebid a 5-card suit unless you are stuck. 2H promises 6 cards here."
    constraints:
      min_hcp: 11
      max_hcp: 15
      shape_requirements: "6+ Hearts"
      evaluation_method: "Length Points"

  - bid: "2S"
    type: "Rebid"
    convention: "Simple Raise"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "12-15 Total Points, 4+ Spades."
    explanation: "We have found a fit! With a minimum hand (12-15), raise partner to the 2-level."
    hint_on_miss: "Support partner's Spades immediately if you have 4 cards."
    constraints:
      min_hcp: 11
      max_hcp: 15
      shape_requirements: "4+ Spades"
      evaluation_method: "Dummy Points"

  - bid: "2NT"
    type: "Rebid"
    convention: "Jump Rebid"
    complexity: "Basic"
    forcing_status: "Forcing"
    inference: "18-19 HCP, Balanced."
    explanation: "A jump to 2NT shows a balanced hand too strong to open 1NT (18-19 HCP)."
    hint_on_miss: "With 18-19 balanced points, you must jump to show your strength."
    constraints:
      min_hcp: 18
      max_hcp: 19
      shape_requirements: "Balanced"
      evaluation_method: "HCP"

  - bid: "3H"
    type: "Rebid"
    convention: "Jump Rebid"
    complexity: "Basic"
    forcing_status: "Forcing"
    inference: "16-18 Total Points, 6+ Hearts."
    explanation: "A jump rebid in your own suit shows a medium strength hand (16-18) and a strong 6-card suit."
    hint_on_miss: "With extra values and a long suit, jump to 3H to invite game."
    constraints:
      min_hcp: 15
      max_hcp: 18
      shape_requirements: "6+ Hearts"
      evaluation_method: "Length Points"

  - bid: "3S"
    type: "Rebid"
    convention: "Limit Raise"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "16-18 Total Points, 4+ Spades."
    explanation: "With a medium hand (16-18) and support, jump raise to invite game."
    hint_on_miss: "You have too much strength for a simple 2S raise. Jump to 3S."
    constraints:
      min_hcp: 15
      max_hcp: 18
      shape_requirements: "4+ Spades"
      evaluation_method: "Dummy Points"

  - bid: "4S"
    type: "Rebid"
    convention: "Game Raise"
    complexity: "Basic"
    forcing_status: "Sign-off"
    inference: "19-21 Total Points, 4+ Spades."
    explanation: "With a maximum hand (19-21) and a fit, bid strictly to game."
    hint_on_miss: "With 19+ points, do not invite. Bid game directly."
    constraints:
      min_hcp: 18
      max_hcp: 21
      shape_requirements: "4+ Spades"
      evaluation_method: "Dummy Points"

  - bid: "4C"
    type: "Rebid"
    convention: "Splinter"
    complexity: "Advanced"
    forcing_status: "Game Forcing"
    inference: "19+ Total Points, 4+ Spades, Singleton/Void in Clubs."
    explanation: "A double jump shift (Splinter) shows excellent support, max values, and shortness in Clubs."
    hint_on_miss: "If you have a max hand and a singleton, use a Splinter to help partner evaluate slam."
    constraints:
      min_hcp: 18
      max_hcp: 21
      shape_requirements: "4+ Spades, Max 1 Club"
      evaluation_method: "Dummy Points"

  - bid: "4D"
    type: "Rebid"
    convention: "Splinter"
    complexity: "Advanced"
    forcing_status: "Game Forcing"
    inference: "19+ Total Points, 4+ Spades, Singleton/Void in Diamonds."
    explanation: "A double jump shift (Splinter) shows excellent support, max values, and shortness in Diamonds."
    hint_on_miss: "If you have a max hand and a singleton, use a Splinter to help partner evaluate slam."
    constraints:
      min_hcp: 18
      max_hcp: 21
      shape_requirements: "4+ Spades, Max 1 Diamond"
      evaluation_method: "Dummy Points"

"1NT":
  - bid: "Pass"
    type: "Response"
    convention: "Natural"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "0-7 HCP, Balanced or Semi-Balanced."
    explanation: "With fewer than 8 HCP and no 5-card major, we do not have enough strength to invite game. We pass 1NT."
    hint_on_miss: "You need at least 8 HCP to invite game. If you are weak and balanced, pass."
    constraints:
      min_hcp: 0
      max_hcp: 7
      shape_requirements: "No 5-card Major"
      evaluation_method: "HCP"

  - bid: "2C"
    type: "Response"
    convention: "Stayman"
    complexity: "Basic"
    forcing_status: "Forcing"
    inference: "8+ HCP, At least one 4-card Major."
    explanation: "Stayman asks opener if they have a 4-card major. You need 8+ HCP (invitational strength) to use this convention."
    hint_on_miss: "With 8+ points and a 4-card major, bid 2C (Stayman) to find a 4-4 major fit."
    constraints:
      min_hcp: 8
      max_hcp: 25
      shape_requirements: "At least one 4-card Major"
      evaluation_method: "HCP"

  - bid: "2D"
    type: "Response"
    convention: "Jacoby Transfer"
    complexity: "Basic"
    forcing_status: "Forcing"
    inference: "0+ HCP, 5+ Hearts."
    explanation: "A bid of 2D is a transfer to Hearts. It shows 5+ cards in Hearts and commands Opener to bid 2H."
    hint_on_miss: "With a 5-card Major, use a Transfer (bid the suit below your suit)."
    constraints:
      min_hcp: 0
      max_hcp: 25
      shape_requirements: "5+ Hearts"
      evaluation_method: "HCP"

  - bid: "2H"
    type: "Response"
    convention: "Jacoby Transfer"
    complexity: "Basic"
    forcing_status: "Forcing"
    inference: "0+ HCP, 5+ Spades."
    explanation: "A bid of 2H is a transfer to Spades. It shows 5+ cards in Spades and commands Opener to bid 2S."
    hint_on_miss: "With a 5-card Major, use a Transfer (bid the suit below your suit)."
    constraints:
      min_hcp: 0
      max_hcp: 25
      shape_requirements: "5+ Spades"
      evaluation_method: "HCP"

  - bid: "2S"
    type: "Response"
    convention: "Extended Transfer"
    complexity: "Basic"
    forcing_status: "Forcing"
    inference: "Transfer to 3C (usually to sign off in a minor)."
    explanation: "A bid of 2S relays to 3C. This is often used to sign off in Clubs or Diamonds with a weak hand."
    hint_on_miss: "Use 2S to transfer to a minor suit if you have a weak hand with a long minor."
    constraints:
      min_hcp: 0
      max_hcp: 7
      shape_requirements: "6+ Clubs or Diamonds"
      evaluation_method: "HCP"

  - bid: "2NT"
    type: "Response"
    convention: "Natural Invitation"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "8-9 HCP, Balanced, No 4-card Major."
    explanation: "This invites partner to Game. It shows 8-9 points and balanced distribution, without a 4-card major."
    hint_on_miss: "With 8-9 points and no major interest, invite game by bidding 2NT."
    constraints:
      min_hcp: 8
      max_hcp: 9
      shape_requirements: "Balanced, No 4-card Major"
      evaluation_method: "HCP"

  - bid: "3NT"
    type: "Response"
    convention: "Natural"
    complexity: "Basic"
    forcing_status: "Sign-off"
    inference: "10-15 HCP, Balanced, No 4-card Major."
    explanation: "With 10-15 HCP, we have enough for game (25+ combined). We bid 3NT directly."
    hint_on_miss: "With 10+ points and no major suit interest, jump directly to Game (3NT)."
    constraints:
      min_hcp: 10
      max_hcp: 15
      shape_requirements: "Balanced, No 4-card Major"
      evaluation_method: "HCP"

  - bid: "4C"
    type: "Response"
    convention: "Gerber"
    complexity: "Basic"
    forcing_status: "Forcing"
    inference: "Ace Asking (after NT opening)."
    explanation: "A jump to 4C directly over 1NT or 2NT is Gerber, asking for Aces."
    hint_on_miss: "If you want to ask for Aces over a NT opening, use Gerber (4C), not Blackwood."
    constraints:
      min_hcp: 16
      max_hcp: 25
      shape_requirements: "Slam Interest"
      evaluation_method: "HCP"

  - bid: "4NT"
    type: "Response"
    convention: "Quantitative"
    complexity: "Advanced"
    forcing_status: "Non-Forcing"
    inference: "Invites 6NT (shows ~16-17 HCP)."
    explanation: "A direct raise to 4NT is not Blackwood. It is a Quantitative invitation asking partner to bid 6NT with a maximum."
    hint_on_miss: "4NT is quantitative here. Bid it with 16-17 points to invite slam."
    constraints:
      min_hcp: 16
      max_hcp: 17
      shape_requirements: "Balanced"
      evaluation_method: "HCP"

"1S":
  - bid: "Pass"
    type: "Response"
    convention: "Natural"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "0-5 HCP."
    explanation: "With fewer than 6 points, we cannot keep the bidding open."
    hint_on_miss: "You need at least 6 points to respond."
    constraints:
      min_hcp: 0
      max_hcp: 5
      shape_requirements: "Any"
      evaluation_method: "HCP"

  - bid: "1NT"
    type: "Response"
    convention: "Natural"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "6-9 HCP, denies 3+ Spades."
    explanation: "The 'dustbin' bid. Shows 6-9 points and denies support for Spades. It implies you don't have a new suit you can bid at the 1-level."
    hint_on_miss: "Without support for Spades and unable to bid a new suit at the 1-level, bid 1NT (6-9)."
    constraints:
      min_hcp: 6
      max_hcp: 9
      shape_requirements: "<3 Spades"
      evaluation_method: "HCP"

  - bid: "2C"
    type: "Response"
    convention: "Natural"
    complexity: "Basic"
    forcing_status: "Forcing"
    inference: "10+ HCP, 5+ Clubs."
    explanation: "A new suit at the 2-level promises 10+ points and usually a 5-card suit."
    hint_on_miss: "You need 10+ points to bid a new suit at the 2-level."
    constraints:
      min_hcp: 10
      max_hcp: 21
      shape_requirements: "5+ Clubs"
      evaluation_method: "HCP"

  - bid: "2D"
    type: "Response"
    convention: "Natural"
    complexity: "Basic"
    forcing_status: "Forcing"
    inference: "10+ HCP, 5+ Diamonds."
    explanation: "A new suit at the 2-level promises 10+ points and usually a 5-card suit."
    hint_on_miss: "You need 10+ points to bid a new suit at the 2-level."
    constraints:
      min_hcp: 10
      max_hcp: 21
      shape_requirements: "5+ Diamonds"
      evaluation_method: "HCP"

  - bid: "2H"
    type: "Response"
    convention: "Natural"
    complexity: "Basic"
    forcing_status: "Forcing"
    inference: "10+ HCP, 5+ Hearts."
    explanation: "A new suit at the 2-level promises 10+ points and usually a 5-card suit. This is NOT a raise; it is a new suit."
    hint_on_miss: "2H is a new suit here (Hearts), not a raise of Spades. You need 10+ points."
    constraints:
      min_hcp: 10
      max_hcp: 21
      shape_requirements: "5+ Hearts"
      evaluation_method: "HCP"

  - bid: "2S"
    type: "Response"
    convention: "Simple Raise"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "6-10 Dummy Points, 3+ Spades."
    explanation: "A minimum raise showing a fit and 6-10 points."
    hint_on_miss: "With 3+ Spades and minimum values, raise directly to 2S."
    constraints:
      min_dummy_points: 6
      max_dummy_points: 10
      shape_requirements: "3+ Spades"
      evaluation_method: "Dummy Points"

  - bid: "2NT"
    type: "Response"
    convention: "Jacoby 2NT"
    complexity: "Advanced"
    forcing_status: "Game Forcing"
    inference: "13+ Dummy Points, 4+ Spades."
    explanation: "Artificial game-forcing raise asking Opener to show shortness."
    hint_on_miss: "With game values and 4+ trumps, use Jacoby 2NT."
    constraints:
      min_dummy_points: 13
      shape_requirements: "4+ Spades"
      evaluation_method: "Dummy Points"

  - bid: "3S"
    type: "Response"
    convention: "Limit Raise"
    complexity: "Basic"
    forcing_status: "Non-Forcing"
    inference: "11-12 Dummy Points, 3+ Spades."
    explanation: "Invitational jump raise. Asks partner to bid game with a maximum."
    hint_on_miss: "With 11-12 points and support, jump to 3S to invite game."
    constraints:
      min_dummy_points: 11
      max_dummy_points: 12
      shape_requirements: "3+ Spades"
      evaluation_method: "Dummy Points"

  - bid: "4C"
    type: "Response"
    convention: "Splinter"
    complexity: "Advanced"
    forcing_status: "Game Forcing"
    inference: "13+ Points, 4+ Spades, Singleton/Void in Clubs."
    explanation: "Double jump shift showing game values, support, and shortness in Clubs."
    constraints:
      min_dummy_points: 13
      shape_requirements: "4+ Spades, Max 1 Club"
      evaluation_method: "Dummy Points"

  - bid: "4D"
    type: "Response"
    convention: "Splinter"
    complexity: "Advanced"
    forcing_status: "Game Forcing"
    inference: "13+ Points, 4+ Spades, Singleton/Void in Diamonds."
    explanation: "Double jump shift showing game values, support, and shortness in Diamonds."
    constraints:
      min_dummy_points: 13
      shape_requirements: "4+ Spades, Max 1 Diamond"
      evaluation_method: "Dummy Points"

  - bid: "4H"
    type: "Response"
    convention: "Splinter"
    complexity: "Advanced"
    forcing_status: "Game Forcing"
    inference: "13+ Points, 4+ Spades, Singleton/Void in Hearts."
    explanation: "Double jump shift showing game values, support, and shortness in Hearts."
    constraints:
      min_dummy_points: 13
      shape_requirements: "4+ Spades, Max 1 Heart"
      evaluation_method: "Dummy Points"

  - bid: "4S"
    type: "Response"
    convention: "Game Raise"
    complexity: "Basic"
    forcing_status: "Sign-off"
    inference: "13+ Dummy Points, usually balanced."
    explanation: "A direct jump to game. Usually denies slam interest."
    hint_on_miss: "If you have game values and no slam interest, bid 4S."
    constraints:
      min_dummy_points: 13
      shape_requirements: "3+ Spades"
      evaluation_method: "Dummy Points"
"""

# Overwrite the corrupted file with the clean string
print("Restoring database to clean state...")
with open("systems/bidding_tree.yaml", "w", encoding='utf-8') as f:
    f.write(YAML_CONTENT)
print("Database restored successfully.")