**\*\*\*How the Win the Day System Is Used in the Mindset Operating
System**

**1. Purpose of Win the Day in the VirtusFocus System**

The **Win the Day (WTD)** system provides a **simple, objective,
repeatable daily scoring model** that teaches athletes to:

* build intentional habits
* strengthen self-regulation
* shift from emotional reactivity to identity-based choices
* track daily consistency
* reflect without shame
* develop momentum through small wins

Each of the 5 daily questions is directly tied to core VirtusFocus
values and behavioral outcomes.



The WTD system is the **anchor of the Evening Review workflow** and is a
mandatory daily action.



**2. Where Win the Day Appears in the App**

**✔ Daily Evening Check-In (Mandatory Step 1)**

The WTD section appears **immediately.** Before journaling input, and
before the Bullseye Method screen.

Athletes answer all **five questions**, each **Yes = 1 point / No = 0
points**.

**✔ Weekly Recap Integration**

Weekly score totals (0--35) are used in:  
• AI coaching analysis  
• determining "Growth," "Mixed," or "Reset" weeks  
• pattern detection (emotional reactivity, follow-through, consistency)  
• streak logic in the athlete dashboard



**3. Daily Win the Day Workflow Detail**

**3.1 Trigger**

The WTD screen appears automatically when the athlete starts the Evening
Review.

**3.2 UI Behavior**

Each question is shown with:  
• the question text (from system file)  
• a short example (contextual learning, optional)  
• a **Yes/No toggle or button pair**  
• optional tooltips for new athletes



**3.3 The Five Daily Questions (with developer notes)**

**Question 1 --- ACT WITH INTENTION? (1 pt)**

Did I act intentionally or was I reactive today?  


**Question 2 --- Complete the Mindset Challenge? (1 pt)**

Did I follow through on the Mindset Challenge set during the morning Tune-Up?  


**Question 3 --- RESPOND TO ADVERSITY WELL? (1 pt)**

Did I respond (not react) when things got hard?  




**Question 4 --- PROGRESS OVER PERFECTION? (1 pt)**

Did I choose growth instead of expecting perfection?  


**Question 5 --- GRATITUDE / SELF-COMPASSION? (1 pt)**

Did I end the day grounded (not self-critical)?  


**4. Scoring Logic**

**Daily Score Calculation**

Total score = Sum of 5 binary answers (0--5).



**6. Athlete Experience**

**6.1 Daily Athlete Flow**

1. Receive Daily Recap reminder
2. Open app → answer 5 Win the Day questions (~15 seconds)
3. Daily Journaling
4. Move into Bullseye Method screen
5. Submit entire Evening Review



**8. Developer Notes / Spec Implications**

**Frontend**

* Yes/No must be one-tap, high clarity



**Backend**  
• raw values per question


**9. V1** 

✔ Five-question daily scoring  
✔ Score calculation \& storage  

