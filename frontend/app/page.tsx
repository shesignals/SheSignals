import Link from 'next/link';
import Image from 'next/image';

export default function Home() {
  return (
    <div className="w-full">
      
      {/* 1. HERO SECTION */}
      <section className="max-w-[1200px] mx-auto px-6 py-20 flex flex-col md:flex-row items-center gap-12">
        <div className="flex-1 text-center md:text-left">
          <span className="inline-block px-4 py-1.5 rounded-full bg-[#fe70d7]/10 text-[#fe70d7] font-semibold text-sm mb-6 border border-[#fe70d7]/20">
            Clinical Decision Support
          </span>
          <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight mb-6 leading-tight text-[var(--text)]">
            Empowering Early Detection of <span className="text-[#fe70d7]">Autism in Girls</span>
          </h1>
          <p className="text-lg md:text-xl text-[var(--muted)] mb-8 leading-relaxed max-w-[600px] mx-auto md:mx-0">
            Welcome to SheSignals. At SheSignals, we are dedicated to helping parents, educators, and clinicians recognize early signs of autism in girls, a population often overlooked due to subtle or masked presentations. Through precise screening tools and a deeper understanding of gender-specific behaviors, SheSignals strives to enable early support, intervention, and empowerment.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
            <Link href="/screening" className="px-8 py-4 bg-[#fe70d7] text-white rounded-xl font-bold text-lg text-center hover:bg-[#d05ab0] transition-colors shadow-lg shadow-[#fe70d7]/20">
                Take Screening
            </Link>
            <Link href="#mission" className="px-8 py-4 bg-[var(--panel)] border border-[var(--border)] text-[var(--text)] rounded-xl font-bold text-lg text-center hover:bg-[var(--btn-bg1)] transition-colors">
                Learn More
            </Link>
          </div>
        </div>
        <div className="flex-1 flex justify-center mt-10 md:mt-0">
          <div className="relative">
             <div className="absolute inset-0 bg-[#fe70d7]/20 blur-3xl rounded-full scale-90"></div>
             <Image src="/center_logo.png" alt="SheSignals Logo" width={400} height={400} priority className="relative z-10 drop-shadow-2xl" />
          </div>
        </div>
      </section>

      {/* 2. MISSION & WHY IT MATTERS (Alternating Split) */}
      <section id="mission" className="bg-[var(--panel)] py-24 border-y border-[var(--border)]">
        <div className="max-w-[1200px] mx-auto px-6">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-3xl font-bold mb-6 text-[var(--text)]">Our Mission</h2>
              <p className="text-lg text-[var(--text)] leading-relaxed mb-6 font-medium">
                To close the diagnostic gap and foster early, accurate identification of autism in girls, allowing them to thrive with timely support.
              </p>
              <h2 className="text-2xl font-bold mb-4 mt-8 text-[var(--text)]">Why Early Detection of Autism in Girls Matters</h2>
              <p className="text-[var(--text)] leading-relaxed mb-4">
                Early detection of autism in girls is critical because autistic traits in females often present differently, more subtly, or are intentionally masked compared to males. Without early identification, girls are at higher risk of experiencing chronic mental health challenges, and delayed access to crucial support systems. Moreover, girls with autism are frequently misdiagnosed or diagnosed later than boys.
              </p>
              <p className="text-[var(--text)] leading-relaxed mb-4">
                Early recognition in girls can be life-changing. It dramatically improves developmental outcomes by enabling access to therapies, support systems, and educational accommodations when they are most impactful.
              </p>
              <p className="text-[var(--text)] leading-relaxed mb-4">
                It is the key to unlocking strengths, navigating challenges, and building a future where autistic girls are fully seen and supported. Early diagnosis is not just about labeling—it is about opening doors to understanding, authentic support, and healthier futures for autistic girls.
              </p>
            </div>
            <div className="bg-[var(--bg)] p-12 rounded-3xl border border-[var(--border)] relative overflow-hidden">
                <div className="absolute top-0 right-0 w-64 h-64 bg-[#fe70d7]/10 blur-3xl rounded-full"></div>
                <h3 className="text-2xl font-bold mb-6 text-[#fe70d7]">Our Technology</h3>
                <p className="text-[var(--text)] leading-relaxed relative z-10">
                  SheSignals uses a layered machine learning approach to analyze structured responses from parents, guardians, and educators across 38 behavioral and developmental indicators. Our models include <strong className="text-[#fe70d7]">Logistic Regression</strong> for interpretable probability scoring, <strong className="text-[#fe70d7]">Random Forests</strong> for identifying complex behavioral interactions, and Gradient Boosting methods such as <strong className="text-[#fe70d7]">XGBoost</strong> to improve prediction accuracy across subtle response patterns that are often harder to detect in girls. By combining these approaches, the system generates a confidence-based recommendation that helps families determine whether seeking a specialist evaluation may be beneficial. The technology is designed to support early awareness and professional follow-up, not replace clinical diagnosis.
                </p>
            </div>
          </div>
        </div>
      </section>

      {/* 3. FACTS (Word to word, Wide Cards) */}
      <section className="py-24 max-w-[1200px] mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4 text-[var(--text)]">Facts about <span className="text-[#fe70d7]">Autism in Girls</span></h2>
        </div>
        
        <div className="grid md:grid-cols-2 gap-6">
          {[
            "1. On average, women experience a 10-year delay in receiving an autism diagnosis from their first presentation to mental health services? This delay is particularly evident in women who exhibit more nuanced autistic traits and do not have intellectual disabilities.",
            "2. A questionnaire conducted by the Autistic Girls Network found that 43% of autistic girls waited up to two years for a diagnosis, while 24% waited more than three years.",
            "3. Autism Spectrum Disorder (ASD) is diagnosed more frequently in males than females, with traditional estimates suggesting a 4:1 male-to-female ratio. However, recent research indicates that this disparity may be due to under-diagnosis in females. Studies have found that nearly 80% of autistic females remain undiagnosed by age 18.",
            "4. In the United States, approximately 1 in 36 child is diagnosed with autism. Boys are nearly four times more likely to be diagnosed than girls, with about 4 in 100 boys and 1 in 100 girls identified as having autism.",
            "5. A 2022 study published in Autism Research found that autistic girls are more likely to first be misdiagnosed with anxiety, depression, borderline personality disorder, or eating disorders before receiving an autism diagnosis.",
            "6. Almost 50% of autistic females surveyed reported receiving a mental health diagnosis before their autism was identified.",
            "7. A 2021 meta-analysis found that late-diagnosed autistic women were three times more likely to experience major depressive disorder, self-harm, or suicidality compared to early-diagnosed individuals.",
            "8. Boys are diagnosed with autism at much higher rates than girls. According to research, about 1 in 42 boys (around 2.4%) are diagnosed with autism, whereas 1 in 189 girls (around 0.5%) are diagnosed. This means boys are about four times more likely to be diagnosed early compared to girls."
          ].map((fact, index) => (
            <div key={index} className="bg-[var(--panel)] p-8 rounded-2xl border border-[var(--border)] hover:border-[#fe70d7]/50 transition-colors shadow-sm flex gap-6 items-start">
              <div className="text-[#fe70d7] font-black text-3xl opacity-80 mt-1">{index + 1}</div>
              <p className="text-[var(--text)] leading-relaxed text-md">{fact.substring(3)}</p>
            </div>
          ))}
        </div>
      </section>

      {/* 4. APPROACH & FOCUS AREAS (Word to Word grids) */}
      <section className="bg-[var(--panel)] py-24 border-y border-[var(--border)]">
        <div className="max-w-[1200px] mx-auto px-6">
          
          <div className="mb-20">
              <h2 className="text-4xl font-bold mb-4 text-[var(--text)]">Our Screening Approach</h2>
              <p className="text-[var(--text)] text-lg mb-8">SheSignals offers a comprehensive, girl-centered early detection framework:</p>
              
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {[
                    "Neurodevelopmental history collection",
                    "Sensory processing pattern analysis",
                    "Social communication and emotional regulation screening",
                    "Masking and camouflaging behavior identification",
                    "Parent, caregiver, and educator collaboration",
                    "Our questions and explanations are tailored to uncover nuanced indicators often missed in standard screening models."
                  ].map((framework, i) => (
                    <div key={i} className="bg-[var(--bg)] p-6 rounded-xl border border-[var(--border)] flex items-start gap-4 hover:border-[#fe70d7]/30 transition-colors">
                        <div className="bg-[#fe70d7]/10 text-[#fe70d7] font-bold rounded-full w-8 h-8 flex items-center justify-center shrink-0">{i + 1}</div>
                        <p className="text-[var(--text)]">{framework}</p>
                    </div>
                  ))}
              </div>
          </div>

          <div>
              <h2 className="text-4xl font-bold mb-8 text-[var(--text)]">Sample Screening Focus Areas</h2>
              <div className="grid md:grid-cols-2 gap-8">
                  <div className="bg-[var(--bg)] p-8 rounded-xl border border-[var(--border)]">
                      <h4 className="font-bold text-[#fe70d7] mb-3 text-2xl">1. Developmental Milestones</h4>
                      <p className="text-[var(--text)]"><span className="font-bold">Why Important:</span> Age-specific expectations help differentiate transient delays from persistent neurodevelopmental patterns.</p>
                  </div>
                  <div className="bg-[var(--bg)] p-8 rounded-xl border border-[var(--border)]">
                      <h4 className="font-bold text-[#fe70d7] mb-3 text-2xl">2. Social Reciprocity and Friendships</h4>
                      <p className="text-[var(--text)]"><span className="font-bold">Why Important:</span> Superficial social fluency can mask deep struggles with peer interactions.</p>
                  </div>
                  <div className="bg-[var(--bg)] p-8 rounded-xl border border-[var(--border)]">
                      <h4 className="font-bold text-[#fe70d7] mb-3 text-2xl">3. Emotional and Sensory Regulation</h4>
                      <p className="text-[var(--text)]"><span className="font-bold">Why Important:</span> Subtle internalized distress can precede overt signs of anxiety and depression.</p>
                  </div>
                  <div className="bg-[var(--bg)] p-8 rounded-xl border border-[var(--border)]">
                      <h4 className="font-bold text-[#fe70d7] mb-3 text-2xl">4. Masking and Camouflaging Behaviors</h4>
                      <p className="text-[var(--text)]"><span className="font-bold">Why Important:</span> Girls often work hard to mimic typical behaviors, leading to later or missed diagnoses.</p>
                  </div>
                  <div className="bg-[var(--bg)] p-8 rounded-xl border border-[var(--border)] md:col-span-2 text-center md:text-left">
                      <h4 className="font-bold text-[#fe70d7] mb-3 text-2xl">5. Family and Medical History</h4>
                      <p className="text-[var(--text)]"><span className="font-bold">Why Important:</span> Genetic and perinatal factors provide critical diagnostic context.</p>
                  </div>
              </div>
          </div>
          
        </div>
      </section>

      {/* 5. RESOURCES & ADVISORS (Word to Word) */}
      <section className="py-24 max-w-[1200px] mx-auto px-6">
        <div className="grid md:grid-cols-2 gap-16">
            <div>
              <h2 className="text-3xl font-bold mb-6 text-[var(--text)]">Resources to Download</h2>
              <p className="text-[var(--text)] mb-8 italic">
                Please note that these resources are for your early awareness. These are not for diagnostic. Our recommendations are meant to encourage you to engage with a qualified medical professional for a timely follow-up.
              </p>
              <div className="flex flex-col gap-4">
                <Link href="/SheSignals_Questions_W_Explanation.pdf" target="_blank" className="flex items-center gap-4 p-5 bg-[var(--panel)] rounded-xl border border-[var(--border)] hover:border-[#fe70d7] transition-all hover:shadow-md hover:shadow-[#fe70d7]/10 group">
                    <div className="w-12 h-12 bg-[#fe70d7]/10 rounded-lg flex items-center justify-center text-[#fe70d7] font-bold group-hover:bg-[#fe70d7] group-hover:text-white transition-colors">PDF</div>
                    <span className="font-semibold text-[var(--text)] text-lg">38 Questions Screening for Parents and Teachers</span>
                </Link>
                <Link href="/SheSignals_Parents_Guidebook.pdf" target="_blank" className="flex items-center gap-4 p-5 bg-[var(--panel)] rounded-xl border border-[var(--border)] hover:border-[#fe70d7] transition-all hover:shadow-md hover:shadow-[#fe70d7]/10 group">
                    <div className="w-12 h-12 bg-[#fe70d7]/10 rounded-lg flex items-center justify-center text-[#fe70d7] font-bold group-hover:bg-[#fe70d7] group-hover:text-white transition-colors">PDF</div>
                    <span className="font-semibold text-[var(--text)] text-lg">A Guidebook for Parents</span>
                </Link>
              </div>
            </div>
            
            <div>
              <h2 className="text-3xl font-bold mb-6 text-[var(--text)]">Advisors</h2>
              <ul className="space-y-4 mb-12">
                <li className="flex flex-col p-5 bg-[var(--panel)] rounded-xl border border-[var(--border)]">
                    <strong className="text-[var(--text)] text-lg">Lauren Levinson</strong>
                    <span className="text-sm text-[#fe70d7] font-medium">Bay Area Friendship Circle</span>
                </li>
                <li className="flex flex-col p-5 bg-[var(--panel)] rounded-xl border border-[var(--border)]">
                    <strong className="text-[var(--text)] text-lg">Sydney Zitzer</strong>
                    <span className="text-sm text-[#fe70d7] font-medium">Pacific Autism Center for Education</span>
                </li>
              </ul>
              <h3 className="text-2xl font-bold mb-6 text-[var(--text)]">Books We Recommend</h3>
              <ol className="list-decimal pl-5 text-[var(--text)] space-y-3 font-medium">
                <li>How to be Autistic by Rachel Morgan-Trimmer</li>
                <li>Autism in Heels: The Untold Story of a female life on the spectrum by Jennifer Cook O’Toole</li>
                <li>But You Don’t Look Autistic At All by Bianca Toeps</li>
                <li>Nobody Nowhere by Donna Williams</li>
              </ol>
            </div>
        </div>
      </section>

      {/* CONTACT US (Word to Word) */}
      <section className="bg-[var(--panel)] py-16 border-t border-[var(--border)] text-center">
        <h2 className="text-3xl font-bold mb-4 text-[var(--text)]">Contact Us</h2>
        <p className="text-[var(--text)] text-lg">
          <strong>Anushka Parekh</strong><br />
          Founder SheSignals, LLC<br />
          <a href="mailto:anushka@shesignals.com" className="text-[#fe70d7] hover:underline font-medium">anushka@shesignals.com</a>
        </p>
      </section>

      {/* 6. GIANT CTA BANNER */}
      <section className="bg-[#fe70d7] py-24 px-6 text-center">
         <h2 className="text-4xl md:text-5xl font-extrabold text-white mb-6">Autism Screening Assessment</h2>
         <p className="text-white/90 text-xl font-medium max-w-[600px] mx-auto mb-10 leading-relaxed">
            Take our comprehensive diagnostic screening to evaluate early signs.
         </p>
         <Link href="/screening" className="inline-block px-12 py-5 bg-white text-[#fe70d7] rounded-xl font-black text-xl hover:bg-gray-100 transition-colors shadow-2xl">
            TAKE SCREENING
         </Link>
      </section>

    </div>
  );
}
