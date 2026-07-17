# -*- coding: utf-8 -*-
import io

days = [
    # Day 1
    [
        ("08:00&ndash;08:30 am", "Breakfast &amp; Registration", ""),
        ("08:30&ndash;09:00 am", "Inauguration, Introduction &amp; Welcome", "Representative from SJNAHS, J. Andoni Urtizberea, Ann Agnes Mathew"),
        ("09:00&ndash;09:45 am", "Introduction to Clinical Myology <span style='color:var(--ink-muted)'>(35&rsquo; talk, 10&rsquo; discussion)</span>", "Satish Khadilkar"),
        ("09:45&ndash;10:30 am", "Practical Approach of a Hypotonic Infant/Child <span style='color:var(--ink-muted)'>(35&rsquo; talk, 10&rsquo; discussion)</span>", "V. Vishwanathan"),
        ("10:30&ndash;10:45 am", "Coffee Break", ""),
        ("10:45 am&ndash;12:45 pm", "Case Studies (Session 1) &mdash; Muscle &middot; 5&ndash;6 didactic cases presented by faculties", "Chair: J. Andoni Urtizberea, V. Vishwanathan, Edoardo, Sruthi, VY Vishnu"),
        ("12:45&ndash;02:00 pm", "Lunch Break", ""),
        ("02:00&ndash;04:30 pm", "Hands-on Parallel Workshops &amp; On-site Visits (Day 1) &mdash; Respiratory Level 1, MDT, Neuropath, Myogenetics Level 1", "Vic, Sneha, Vinitha, Mahima, NIMHANS, Sanjeeva, Supriya, Ilin"),
        ("04:30&ndash;04:45 pm", "Coffee Break", ""),
        ("04:45&ndash;06:00 pm", "From Bench to Bedside in Duchenne MD <span style='color:var(--ink-muted)'>(60&rsquo; talk, 15&rsquo; discussion)</span> &mdash; How to bring cutting-edge therapies to the patient", "Annemieke Aartsma-Rus"),
        ("06:30 pm", "Networking Reception &amp; Dinner", "Venue: St. John&rsquo;s Research Institute, St. John&rsquo;s National Academy of Health Sciences, Bangalore"),
    ],
    # Day 2
    [
        ("09:00&ndash;09:45 am", "Congenital Muscular Dystrophy <span style='color:var(--ink-muted)'>(35&rsquo; talk, 10&rsquo; discussion)</span>", "Renu Suthar"),
        ("09:45&ndash;10:30 am", "Congenital Myopathies <span style='color:var(--ink-muted)'>(35&rsquo; talk, 10&rsquo; discussion)</span>", "Edoardo Malfatti"),
        ("10:30&ndash;10:45 am", "Coffee Break", ""),
        ("10:45 am&ndash;12:45 pm", "Case Studies (Session 2) &mdash; Motor Neurone &middot; 5&ndash;6 didactic cases presented by faculties", "Andoni: Sruthi, Ann, Vineeth Jaison, Vishnu"),
        ("12:45&ndash;02:00 pm", "Lunch Break", ""),
        ("02:00&ndash;04:30 pm", "Hands-on Workshops (Day 2) &mdash; Neurophysiology 1 (&times;2), Myogenetics Level 1, Imaging", "Suma, Thabit, Vinitha, Abhilash, Sneha, Kushnuma, Nandedkar, Radhika, Umesh, Lokesh &amp; Akshata, Seena &mdash; Chair: Edoardo"),
        ("04:30&ndash;04:45 pm", "Coffee Break", ""),
        ("04:45&ndash;06:00 pm", "Dysferlinopathies &amp; Limb Girdle Muscular Dystrophy <span style='color:var(--ink-muted)'>(60&rsquo; talk, 15&rsquo; discussion)</span>", "Andoni Urtizberea"),
        ("06:30 pm", "End of Day 2 &mdash; Dinner / Meet the Speakers", ""),
    ],
    # Day 3
    [
        ("09:00&ndash;09:45 am", "Charcot Marie Tooth Disease <span style='color:var(--ink-muted)'>(35&rsquo; talk, 10&rsquo; discussion)</span>", "Urvi Desai"),
        ("09:45&ndash;10:30 am", "Dysimmune Neuropathies (GBS, CIDP, &hellip;) <span style='color:var(--ink-muted)'>(35&rsquo; talk, 10&rsquo; discussion)</span>", "Umesh Kalane"),
        ("10:30&ndash;10:45 am", "Coffee Break", ""),
        ("10:45 am&ndash;12:45 pm", "Case Studies (Session 3) &mdash; Neuropathy &middot; 5&ndash;6 didactic cases presented by faculties", "Chair: Urvi, Andoni, Umesh, Vishnu, Sruthi, Radhika"),
        ("12:45&ndash;02:00 pm", "Lunch Break (Room 1) &mdash; Group Photo", ""),
        ("02:00&ndash;04:30 pm", "Hands-on Workshops (Day 3) &mdash; Imaging, Neurophysiology 2 (&times;2), Myogenetics Level 2", "Annemieke, Sruthi, Urvi, Gauri Krishna, Andoni, Vishnu"),
        ("04:30&ndash;04:45 pm", "Coffee Break", ""),
        ("04:45&ndash;06:00 pm", "Electrophysiology Applied to Nerve &amp; Muscle Disorders <span style='color:var(--ink-muted)'>(60&rsquo; talk, 15&rsquo; discussion)</span>", "Sanjeev, Radhika"),
        ("06:30 pm", "End of Day 3 / Dinner &amp; Meet the Experts", ""),
    ],
    # Day 4
    [
        ("09:00&ndash;09:45 am", "Dystrophic and Non-Dystrophic Myotonias <span style='color:var(--ink-muted)'>(35&rsquo; talk, 10&rsquo; discussion)</span>", "Sruthi Nair"),
        ("09:45&ndash;10:30 am", "Pompe &amp; Metabolic Myopathies <span style='color:var(--ink-muted)'>(35&rsquo; talk, 10&rsquo; discussion)</span>", "Gauri Krishna"),
        ("10:30&ndash;10:45 am", "Coffee Break", ""),
        ("10:45 am&ndash;12:45 pm", "Case Studies (Session 4) &mdash; NMJ &middot; 5&ndash;6 didactic cases presented by faculties", "Edoardo, Andoni, Umesh, Urvi, Radhika, Sruthi, Vineeth"),
        ("12:45&ndash;02:00 pm", "Lunch Break", ""),
        ("02:00&ndash;04:15 pm", "Hands-on Workshops &amp; On-site Visits (Day 4) &mdash; Respiratory 2, Neuropath, Neurophysiology 1, Myogenetics Level 2", "Sruthi (Neuropath)"),
        ("04:30&ndash;04:45 pm", "Coffee Break", ""),
        ("04:45&ndash;06:15 pm", "FSHD and Repeat Disorders in NMD (DM1, DM2, NDM, others) <span style='color:var(--ink-muted)'>(60&rsquo; talk, 15&rsquo; discussion)</span>", "VY Vishnu"),
        ("06:30 pm", "Networking Dinner / Meet the Experts &mdash; Summer Dinner (Grand Mercure)", ""),
    ],
    # Day 5
    [
        ("09:00&ndash;09:45 am", "Therapeutics in SMA &amp; Update <span style='color:var(--ink-muted)'>(35&rsquo; talk, 10&rsquo; discussion)</span>", "Kumaran Deiva"),
        ("09:45&ndash;10:30 am", "Newest Experimental Therapeutic Approaches in Muscular Dystrophies &mdash; DMD, LGMD, CMD, SMA in Skeletal Muscle &amp; Brain <span style='color:var(--ink-muted)'>(35&rsquo; talk, 10&rsquo; discussion)</span>", "Joanne Ng"),
        ("10:30&ndash;10:45 am", "Coffee Break", ""),
        ("10:45 am&ndash;12:45 pm", "Case Studies (Session 5) &mdash; Pot Pourri &middot; 5&ndash;6 didactic cases presented by faculties", "Kumaran Deiva, Andoni, Vineeth, Urvi, Vishnu"),
        ("12:45&ndash;02:00 pm", "Lunch Break", ""),
        ("02:00&ndash;04:30 pm", "Hands-on Workshops (Day 5) &mdash; Rehab, Respiratory 2, Myogenetics 2, Clinical Research Primer", ""),
        ("04:30&ndash;04:45 pm", "Coffee Break", ""),
        ("04:45&ndash;06:00 pm", "Myasthenia Gravis and Novel Therapies <span style='color:var(--ink-muted)'>(60&rsquo; talk, 15&rsquo; discussion)</span>", "Dr. Urvi Desai"),
        ("06:30 pm", "End of Day 5 / Meet the Speakers &amp; Dinner", ""),
    ],
    # Day 6
    [
        ("09:00&ndash;09:45 am", "Serving the Underserved &mdash; Multidisciplinary Approach in DMD as a Prototype <span style='color:var(--ink-muted)'>(35&rsquo; talk, 10&rsquo; discussion)</span>", "Vineeth Jaison"),
        ("09:45&ndash;10:30 am", "Congenital Myasthenia <span style='color:var(--ink-muted)'>(35&rsquo; talk, 10&rsquo; discussion)</span>", "Nalini Atchayaram"),
        ("10:30&ndash;10:45 am", "Coffee Break", ""),
        ("10:45 am&ndash;12:45 pm", "Case Studies &mdash; Challenging Cases &middot; 5&ndash;6 solved or unsolved cases presented by participants", "Andoni, Edoardo, Sruthi, Kumaran Deiva, Vineeth, Vishnu"),
        ("12:45&ndash;02:00 pm", "Lunch Break", ""),
        ("02:00&ndash;04:30 pm", "Hands-on Workshops &amp; On-site Visit &mdash; Neuropath, Neurophysiology 2, Respiratory 1, Rehab", ""),
        ("04:30&ndash;04:45 pm", "Coffee Break", ""),
        ("04:45&ndash;06:30 pm", "GNE Myopathies and Riboflavinopathies <span style='color:var(--ink-muted)'>(60&rsquo; talk, 15&rsquo; discussion)</span>", "Andoni Urtizberea"),
        ("06:30 pm", "End of Day 6 / Meet the Speakers &amp; Dinner", ""),
    ],
    # Day 7
    [
        ("09:00&ndash;09:45 am", "Trial Readiness in NMD <span style='color:var(--ink-muted)'>(35&rsquo; talk, 10&rsquo; discussion)</span>", "Ramya R Babu"),
        ("09:45&ndash;10:30 am", "Round Table: An Ideal MDT <span style='color:var(--ink-muted)'>(35&rsquo; talk, 10&rsquo; discussion)</span>", "Ann Agnes Mathew, Supriya, Suma, Saravanan, Jayanth Sampath, Murali Mohan, Vinitha"),
        ("10:30&ndash;10:45 am", "Coffee Break", ""),
        ("10:45 am&ndash;12:45 pm", "Case Studies (Session 6) &mdash; Cases with MDT Vignettes &middot; 5&ndash;6 MDT troubles in NMD", "Presented by Allied Specialists (All)"),
        ("12:45&ndash;01:30 pm", "Lunch Break", ""),
        ("01:30&ndash;04:00 pm", "Parallel Workshop &mdash; MDT, Respiratory 2, Clinical Research Primer", ""),
        ("04:00&ndash;04:30 pm", "Quiz", "J. Andoni Urtizberea"),
        ("04:30&ndash;05:00 pm", "Closing Ceremony, Wrap Up &amp; Certificates", ""),
    ],
]

def build():
    out = ['<div class="schedule-panels">']
    for i, sessions in enumerate(days):
        active = " active" if i == 0 else ""
        out.append('  <div class="schedule-panel%s" id="sched-panel-%d">' % (active, i))
        out.append('    <div class="schedule-columns" style="grid-template-columns:1fr;">')
        out.append('      <div class="schedule-col">')
        for time, title, speaker in sessions:
            row = '<div class="session-row"><div class="session-time">%s</div><div class="session-title">%s</div>' % (time, title)
            if speaker:
                row += '<div class="session-speaker">%s</div>' % speaker
            row += '</div>'
            out.append(row)
        out.append('      </div>')
        out.append('    </div>')
        out.append('  </div>')
    out.append('</div>')
    return "\n".join(out) + "\n"

with io.open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

start_marker = '<div class="schedule-panels">'
end_marker = '    <div class="schedule-note">'
si = html.index(start_marker)
ei = html.index(end_marker)
new_html = html[:si] + build() + "\n" + html[ei:]

with io.open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("Replaced schedule panels. Old block length:", ei - si, "New:", len(build()))
