**\*\*\*How the Weekly Motivation Inventory Is Used in the
Mindset Operating System**

**1. Purpose of the Motivation Inventory System**

The **Motivation Inventory** is the qualitative, weekly reflection
module inside the VirtusFocus Weekly Recap.  
It captures:

* **What motivated the athlete this week**
* **What they achieved**
* **Which Mindset Challenge resonated most**
* **What goals they are setting for the next week**
* **Any relevant context for coaches**
* **Competition schedules**

This Inventory serves three main purposes:

**A. Coaching Insight**

The AI Coach uses Motivation Inventory entries to identify:

* Goal alignment vs. drift
* Identity-language strength
* Consistency of motivation
* Self-leadership markers
* Emotional and environmental influences
* Readiness for deeper challenge or intervention
* Red flags (avoidance, overwhelm, low motivation)

These are required elements of the weekly coaching analysis.


**B. Athlete Ownership**

The weekly questions help athletes:

* Reflect on progress in a structured way
* Build momentum week to week
* Connect Tune-Ups to outcomes
* Reaffirm their goals
* Strengthen identity-based motivation



**C. Data Integration**

Motivation Inventory entries become inputs for:

* AI weekly analysis
* Coach dashboards as an AI summary
* Trend detection (across months/seasons)
* Goal progression tracking

They pair with:

* Win the Day data
* Daily Journals
* Bullseye Method entries

to create a complete weekly psychological profile.



**2. Where the Motivation Inventory Lives in the App**

**✔ Weekly Recap (Sunday)**

It is the **first section** (I'm not sure how to "final organize"
these?) of the Weekly Recap form.

Weekly Recap Flow (FRD):

1. **Motivation Inventory**
2. Confidence \& habit ratings
3. Additional questions (challenges etc may be handled in motivation
   section)
4. Submit → AI Coaching Review triggers automatically



**3. Weekly Motivation Inventory Questions (Developer Detail)**



**Q1 --- What did you achieve this week?**

Athletes reflect on:

* physical progress
* mindset improvements
* habit consistency
* personal growth
* academic wins
* leadership behaviors

**Examples from screenshots:**

* "Got in better wrestling shape"
* "Sharpened my mind"
* "Got my assignments done even when I didn't want to"
* "Recovered my body and built stronger relationships"

**Developer Notes**

* Free text field
* No minimum character rule 
* Stored verbatim for AI analysis



**Q2 --- What was your favorite Mindset Challenge from this week's
Tune-Ups?**

Purpose:

* Reveals which Tune-Up content resonates
* Shows the motivational style that works for the athlete
* Helps AI detect identity and values

Examples:

* "Take one bold step today"
* "Put phone away for 30 minutes and do task"
* "Optimistic Athletes See the Game Differently"

**Developer Notes**

* Free text input

System should link chosen challenge to the Tune-Up dataset 



**Q3 --- What are your goals for the upcoming week?**

Purpose:

* Tracks forward momentum
* Aligns goals with identity statements
* Shows if goals are: vague, habit-based, or identity-based
* Helps AI assign weekly challenge or redirect

Examples:

* "Get stronger," "Go to sleep early," "Prioritize sleep"
* "Finish strong before Thanksgiving"
* "Eat better meals"
* "Get closer to my goals"

**Developer Notes**

* Free text field
* Multi-line
* Required for Recap submission





**Q4 --- Tell me anything else that may be relevant this week**

Purpose:

* Provides emotional and environmental context
* Reveals obstacles, stressors, health issues, schedule changes
* Helps AI coach with empathy while still challenging the athlete

Examples:

* "Gym closed for Memorial Day"
* "I need to lock in on my sleep though"
* "Nothing"

**Developer Notes**

* Free text
* Optional field
* Must be stored for AI context but not required for basic analytics



**Q5 --- List any competitions scheduled for the coming week**

Purpose:

* Allows the app to identify **competition weeks**
* Enables tailored coaching (future)
* Helps coaches plan support
* Adds context for emotional regulation and performance behavior

Examples:

* "None"
* "N/A"
* (Sometimes blank --- must still be allowed)

**Developer Notes**

* Free text field
* Optional
* Should accept "none," "N/A," or empty



**6. Athlete Experience Requirements**

The Motivation Inventory should feel:

* simple
* clear
* encouraging
* reflective
* low friction (<1-2 minutes)



**UI Requirements:**

* Multi-field weekly form
* Save states between fields
* Clear summary at bottom before submission
* Ability to edit answers before final submission



**Tone:**

* Calm
* Direct
* Growth-oriented
* Non-shaming



**8. Developer Notes \& Integration Requirements**

**Frontend**

* 5 questions with large text fields
* Auto-save
* Multi-line input
* Soft character mins/limits (optional)



**Backend**

* Store weekly entries
* Link to date range (Mon--Sun or Sun--Sat depending on system config)
* Ensure compatibility with coaching prompt structure



**9. Roadmap** v**1 (Required for Launch)**

✔ Basic Motivation Inventory form  
✔ Weekly storage + retrieval  
✔ Integrated into AI coaching pipeline  
✔ Coach dashboard visibility (team use AI Summary)





