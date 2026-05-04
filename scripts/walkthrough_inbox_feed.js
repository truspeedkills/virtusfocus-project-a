  function renderInboxFeed() {
    // Walkthrough demo: real Athlete A (Grace Kindel) Week 12 content (Apr 20-26, 2026).
    // - Daily snippets below are REPRESENTATIVE EXAMPLES — no live Stage 6 snippet
    //   exists for this week yet. Voice-matched to the daily content model
    //   (Coach Arron, compressed, bridges yesterday-to-today, no goals).
    // - Weekly Coaching Message body is verbatim from
    //   Focus Group Materials/Athlete Materials/Grace Kindel/
    //     Grace_Kindel_2026-04-20to2026-04-26_VF_CoachingMessage.txt
    //   (salutation "Grace," dropped because in-app context makes it redundant;
    //   "Coach Arron" sign-off rendered by the helper, not the body).
    // - Deep Dive teaser is the actual first paragraph of the Wk12 Mindset
    //   Summary from
    //     Grace_Kindel_2026-04-20to2026-04-26_VF_DeepDive.txt
    return `${statusBar('8:15')}
    <div style="padding-bottom:80px;">
      ${topBar('Messages')}

      <div style="padding:4px 20px 0;">
        ${weekDivider('This Week — Apr 20–26')}

        ${msgDailyMicro({
          time: 'Today, 8:12 AM',
          body: 'Yesterday the warmups came through and the coaches saw it. The result didn\'t change. That sequence is real, and it\'s still real today.',
          isNew: true,
        })}

        ${msgDailyMicro({
          time: 'Thursday, 8:10 AM',
          body: 'Yesterday you got every bunt down on the first pitch and knew it before anyone said it. That noticing is the rep, and you have the same chance to run it today.',
        })}

        ${msgWeeklyCoaching({
          weekLabel: 'Week 12 — Apr 20–26',
          body: 'Wednesday is the week. You wrote, "fast asf today tbh, got all my mf bunts down." That\'s the first time in this program you\'ve named your own work that way without me asking the question first. You said you could feel it. You said you knew the people who needed to see it were watching.<br><br>Then by Sunday you wrote the whole thing out: "I did so good, and it still just like doesnt matter. but i cant say it doesnt matter because like it does, its just annoying but once again oh well." That sentence holds the last six weeks in one place. The work was visible. The coaches saw. The outcome didn\'t change. You kept going anyway.<br><br>That last part is what the program has been building toward. When you walked in here, the goal you wrote for yourself was staying confident in your ability during competition. Back then, confidence came from being on the field. This week it came from naming your own work, hearing the silence after, and continuing anyway. That\'s confidence that doesn\'t need the field to confirm it, Grace.<br><br>The recovery from last weekend\'s two days showed up too. You said you were going to sit with the mindset emails each day. You did. Every day this week paired a prompt with something specific you were working on. That\'s the commitment we set last week, run for the full seven.<br><br>You ended the recap with "idk at this point give me something." Fair. Two games left.',
          actionText: 'Before warmup begins on Friday and Saturday, write down one specific physical cue you\'re going to execute that day. A hitting cue. A throwing target. A footwork drill. The Wednesday standard, applied to one thing per game. After the game, write one sentence on how it showed up. Two games, two cues, two sentences. Whether you play or not, those reps are yours.<br><br>The work is yours, Grace. Run the last two with it.',
          focusQuestion: '"Wednesday you did the work and the people who needed to see it did. The result still didn\'t change. What\'s the part of that work that\'s still worth running through the final two games?"',
        })}

        ${msgDeepDivePreview({
          weekLabel: 'Week 12',
          teaser: 'This was the week your work showed up where it had to and you named it yourself. Wednesday in practice, you got every bunt down on the first pitch, you felt fast out of the box, and you wrote it without anyone prompting you to. By Sunday you wrote the rest of it out: that you did well, that the coaches saw, and that the result still didn\'t change. The full picture of what happened, in your own words.',
          isNew: true,
        })}

        <!-- End of feed -->
        <div style="padding:28px 0 20px;text-align:center;">
          <span style="font-size:13px;color:#3f3f46;">That's everything from this week.</span>
        </div>
      </div>
    </div>
    ${bottomNavInbox()}`;
  }
