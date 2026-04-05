import Link from 'next/link';
import Image from 'next/image';
import { ExpandableSection } from './components/ExpandableSection';

export default function Home() {
  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "2rem", lineHeight: "1.6" }}>
      
      {/* Intro & Mission (Always visible) */}
      <section style={{ textAlign: "center", marginBottom: "3rem" }}>
        <Image src="/center_logo.png" alt="Application Logo" width={200} height={200} priority style={{ display: "inline-block", marginBottom: "1.5rem" }} />
        <h1 style={{ fontSize: "2.5rem", fontWeight: 800, marginBottom: "1.5rem", color: "#fe70d7" }}>
          Empowering Early Detection of Autism in Girls
        </h1>
        <p style={{ fontSize: "1.1rem", color: "var(--text)", marginBottom: "1.5rem" }}>
          Welcome to SheSignals. At SheSignals, we are dedicated to helping parents, educators, and clinicians recognize early signs of autism in girls, a population often overlooked due to subtle or masked presentations. Through precise screening tools and a deeper understanding of gender-specific behaviors, SheSignals strives to enable early support, intervention, and empowerment.
        </p>
        <p>
          <strong style={{ color: "#fe70d7" }}>Our Mission:</strong> To close the diagnostic gap and foster early, accurate identification of autism in girls, allowing them to thrive with timely support.
        </p>
      </section>

      {/* Autism Screening Assessment (CTA - Always visible) */}
      <section style={{ marginBottom: "3rem", textAlign: "center", padding: "2rem", border: "1px solid rgba(254,112,215,0.5)", borderRadius: "12px", background: "var(--panel)" }}>
        <h2 style={{ fontSize: "1.5rem", color: "#fe70d7", marginBottom: "1rem" }}>Autism Screening Assessment</h2>
        <p style={{ marginBottom: "2rem", color: "var(--text)" }}>Take our comprehensive diagnostic screening to evaluate early signs.</p>
        <Link href="/screening">
            <button style={{ padding: "12px 24px" }}>TAKE SCREENING</button>
        </Link>
      </section>

      {/* Expandable Sections */}
      <ExpandableSection title="Why Early Detection in Girls Matters">
        <p style={{ marginBottom: "1rem" }}>
          Early detection of autism in girls is critical because autistic traits in females often present differently, more subtly, or are intentionally masked compared to males. Without early identification, girls are at higher risk of experiencing chronic mental health challenges, and delayed access to crucial support systems. Moreover, girls with autism are frequently misdiagnosed or diagnosed later than boys.
        </p>
        <p style={{ marginBottom: "1rem" }}>
          Early recognition in girls can be life-changing. It dramatically improves developmental outcomes by enabling access to therapies, support systems, and educational accommodations when they are most impactful.
        </p>
        <p>
          It is the key to unlocking strengths, navigating challenges, and building a future where autistic girls are fully seen and supported. Early diagnosis is not just about labeling—it is about opening doors to understanding, authentic support, and healthier futures for autistic girls.
        </p>
      </ExpandableSection>

      <ExpandableSection title="Facts about Autism in Girls">
        <ol style={{ paddingLeft: "1.5rem", margin: 0 }}>
          <li style={{ marginBottom: "0.5rem" }}>On average, women experience a 10-year delay in receiving an autism diagnosis from their first presentation to mental health services. This delay is particularly evident in women who exhibit more nuanced autistic traits and do not have intellectual disabilities.</li>
          <li style={{ marginBottom: "0.5rem" }}>A questionnaire conducted by the Autistic Girls Network found that 43% of autistic girls waited up to two years for a diagnosis, while 24% waited more than three years.</li>
          <li style={{ marginBottom: "0.5rem" }}>Autism Spectrum Disorder (ASD) is diagnosed more frequently in males than females, with traditional estimates suggesting a 4:1 male-to-female ratio. However, recent research indicates that this disparity may be due to under-diagnosis in females. Studies have found that nearly 80% of autistic females remain undiagnosed by age 18.</li>
          <li style={{ marginBottom: "0.5rem" }}>In the United States, approximately 1 in 36 children is diagnosed with autism. Boys are nearly four times more likely to be diagnosed than girls, with about 4 in 100 boys and 1 in 100 girls identified as having autism.</li>
          <li style={{ marginBottom: "0.5rem" }}>A 2022 study published in Autism Research found that autistic girls are more likely to first be misdiagnosed with anxiety, depression, borderline personality disorder, or eating disorders before receiving an autism diagnosis.</li>
          <li style={{ marginBottom: "0.5rem" }}>Almost 50% of autistic females surveyed reported receiving a mental health diagnosis before their autism was identified.</li>
          <li style={{ marginBottom: "0.5rem" }}>A 2021 meta-analysis found that late-diagnosed autistic women were three times more likely to experience major depressive disorder, self-harm, or suicidality compared to early-diagnosed individuals.</li>
          <li>Boys are diagnosed with autism at much higher rates than girls. According to research, about 1 in 42 boys (around 2.4%) are diagnosed with autism, whereas 1 in 189 girls (around 0.5%) are diagnosed. This means boys are about four times more likely to be diagnosed early compared to girls.</li>
        </ol>
      </ExpandableSection>

      <ExpandableSection title="Our Screening Approach">
        <p style={{ marginBottom: "1rem" }}>SheSignals offers a comprehensive, girl-centered early detection framework:</p>
        <ol style={{ paddingLeft: "1.5rem", margin: 0 }}>
          <li style={{ marginBottom: "0.5rem" }}>Neurodevelopmental history collection</li>
          <li style={{ marginBottom: "0.5rem" }}>Sensory processing pattern analysis</li>
          <li style={{ marginBottom: "0.5rem" }}>Social communication and emotional regulation screening</li>
          <li style={{ marginBottom: "0.5rem" }}>Masking and camouflaging behavior identification</li>
          <li style={{ marginBottom: "0.5rem" }}>Parent, caregiver, and educator collaboration</li>
          <li>Our questions and explanations are tailored to uncover nuanced indicators often missed in standard screening models.</li>
        </ol>
      </ExpandableSection>

      <ExpandableSection title="Sample Screening Focus Areas">
        <ol style={{ paddingLeft: "1.5rem", margin: 0 }}>
          <li style={{ marginBottom: "1rem" }}>
            <strong style={{ color: "var(--text)" }}>Developmental Milestones</strong><br/>
            <span style={{ color: "var(--muted)" }}>Why Important: Age-specific expectations help differentiate transient delays from persistent neurodevelopmental patterns.</span>
          </li>
          <li style={{ marginBottom: "1rem" }}>
            <strong style={{ color: "var(--text)" }}>Social Reciprocity and Friendships</strong><br/>
            <span style={{ color: "var(--muted)" }}>Why Important: Superficial social fluency can mask deep struggles with peer interactions.</span>
          </li>
          <li style={{ marginBottom: "1rem" }}>
            <strong style={{ color: "var(--text)" }}>Emotional and Sensory Regulation</strong><br/>
            <span style={{ color: "var(--muted)" }}>Why Important: Subtle internalized distress can precede overt signs of anxiety and depression.</span>
          </li>
          <li style={{ marginBottom: "1rem" }}>
            <strong style={{ color: "var(--text)" }}>Masking and Camouflaging Behaviors</strong><br/>
            <span style={{ color: "var(--muted)" }}>Why Important: Girls often work hard to mimic typical behaviors, leading to later or missed diagnoses.</span>
          </li>
          <li>
            <strong style={{ color: "var(--text)" }}>Family and Medical History</strong><br/>
            <span style={{ color: "var(--muted)" }}>Why Important: Genetic and perinatal factors provide critical diagnostic context.</span>
          </li>
        </ol>
      </ExpandableSection>

      <ExpandableSection title="Resources to Download">
        <p style={{ fontStyle: "italic", marginBottom: "1.5rem", color: "var(--muted)" }}>
          Please note that these resources are for your early awareness. These are not for diagnostic. Our recommendations are meant to encourage you to engage with a qualified medical professional for a timely follow-up.
        </p>
        <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
            <Link href="/SheSignals_Questions_W_Explanation.pdf" target="_blank" style={{ color: "#fe70d7", textDecoration: "underline" }}>
                38 Questions Screening for Parents and Teachers
            </Link>
            <Link href="/SheSignals_Parents_Guidebook.pdf" target="_blank" style={{ color: "#fe70d7", textDecoration: "underline" }}>
                A Guidebook for Parents
            </Link>
        </div>
      </ExpandableSection>

      <ExpandableSection title="Our Technology">
        <p style={{ margin: 0 }}>
          SheSignals uses a layered machine learning approach to analyze structured responses from parents, guardians, and educators across 38 behavioral and developmental indicators. Our models include Logistic Regression for interpretable probability scoring, Random Forests for identifying complex behavioral interactions, and Gradient Boosting methods such as XGBoost to improve prediction accuracy across subtle response patterns that are often harder to detect in girls. By combining these approaches, the system generates a confidence-based recommendation that helps families determine whether seeking a specialist evaluation may be beneficial. The technology is designed to support early awareness and professional follow-up, not replace clinical diagnosis.
        </p>
      </ExpandableSection>

      <ExpandableSection title="Advisors & Recommendations">
        <div style={{ marginBottom: "2rem" }}>
          <h3 style={{ color: "var(--text)", marginBottom: "0.5rem" }}>Advisors</h3>
          <p style={{ margin: 0 }}><strong>Lauren Levinson</strong> — Bay Area Friendship Circle</p>
          <p style={{ margin: 0 }}><strong>Sydney Zitzer</strong> — Pacific Autism Center for Education</p>
        </div>
        <div>
          <h3 style={{ color: "var(--text)", marginBottom: "0.5rem" }}>Books We Recommend</h3>
          <ol style={{ paddingLeft: "1.5rem", margin: 0 }}>
            <li style={{ marginBottom: "0.25rem" }}>How to be Autistic by Rachel Morgan-Trimmer</li>
            <li style={{ marginBottom: "0.25rem" }}>Autism in Heels: The Untold Story of a female life on the spectrum by Jennifer Cook O’Toole</li>
            <li style={{ marginBottom: "0.25rem" }}>But You Don’t Look Autistic At All by Bianca Toeps</li>
            <li>Nobody Nowhere by Donna Williams</li>
          </ol>
        </div>
      </ExpandableSection>

      <ExpandableSection title="Contact Us">
        <p style={{ margin: 0 }}>
          <strong>Anushka Parekh</strong><br/>
          Founder SheSignals, LLC<br/>
          <a href="mailto:anushka@shesignals.com" style={{ color: "#fe70d7", textDecoration: "underline" }}>anushka@shesignals.com</a>
        </p>
      </ExpandableSection>

    </div>
  );
}
