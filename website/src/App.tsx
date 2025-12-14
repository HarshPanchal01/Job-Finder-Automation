import { useEffect, useRef } from "react";
import logo from "./assets/automationLogo.png";
import configureGIF from "./assets/ConfigureAnimation.gif";
import weeklyReportGIF from "./assets/CleanWeeklyReportAnimation.gif";
import automatedDiscoveryGIF from "./assets/AutomatedDiscoveryAnimation.gif";

export default function App() {
  const tickerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const track = tickerRef.current;
    if (!track) return;

    // duplicate content once for infinite scroll
    if (!track.dataset.duplicated) {
      track.innerHTML += track.innerHTML;
      track.dataset.duplicated = "true";
    }

    let y = 0;
    const speed = 0.4;
    let paused = false;

    const container = track.parentElement;

    const onEnter = () => (paused = true);
    const onLeave = () => (paused = false);

    container?.addEventListener("mouseenter", onEnter);
    container?.addEventListener("mouseleave", onLeave);

    let rafId = 0;
    const animate = () => {
      if (!paused) {
        y += speed;
        const half = track.scrollHeight / 2;
        if (y >= half) y = 0;
        track.style.transform = `translateY(${-y}px)`;
      }
      rafId = requestAnimationFrame(animate);
    };

    rafId = requestAnimationFrame(animate);

    return () => {
      container?.removeEventListener("mouseenter", onEnter);
      container?.removeEventListener("mouseleave", onLeave);
      cancelAnimationFrame(rafId);
    };
  }, []);

  return (
    <main className="min-h-screen bg-neutral-950 text-white antialiased scroll-smooth">
      {/* HEADER */}
      <header className="sticky top-0 z-50 border-b border-white/10 bg-neutral-950/70 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <img src={logo} alt="Job Finder Automation" className="h-9 w-9" />
            <span className="text-sm font-semibold tracking-wide">
              Job Finder Automation
            </span>
          </div>

          <nav className="flex items-center gap-3 text-sm">
            <a
              href="#how"
              className="text-white/70 hover:text-white transition"
            >
              How it works
            </a>
            <a
              href="https://github.com/HarshPanchal01/Job-Finder-Automation"
              target="_blank"
              rel="noreferrer"
              className="rounded-lg border border-white/15 px-4 py-2 text-white/80 hover:border-white/30 transition"
            >
              GitHub
            </a>
          </nav>
        </div>
      </header>

      {/* HERO */}
      <section className="relative overflow-hidden">
        <div className="mx-auto max-w-6xl px-6 py-32">
          <h1 className="text-5xl md:text-6xl font-semibold tracking-tight leading-tight">
            Job searching,
            <br />
            <span className="text-yellow-200/80">without the noise.</span>
          </h1>

          <p className="mt-6 max-w-xl text-lg text-white/70">
            A quiet automation that scans job boards, filters aggressively,
            removes duplicates, and delivers a clean weekly report.
          </p>

          <div className="mt-10 flex gap-4">
            <a
              href="#how"
              className="rounded-xl bg-yellow-400 px-6 py-3 text-black font-medium hover:bg-yellow-300 transition"
            >
              See how it works
            </a>
            <a
              href="https://github.com/HarshPanchal01/Job-Finder-Automation"
              target="_blank"
              rel="noreferrer"
              className="rounded-xl border border-white/20 px-6 py-3 text-white/80 hover:border-white/40 transition"
            >
              View GitHub
            </a>
          </div>
        </div>

        <div className="absolute inset-0 -z-10 bg-gradient-to-b from-yellow-400/15 via-transparent to-transparent" />
      </section>

      {/* HOW IT WORKS */}
      <section id="how" className="border-t border-white/10">
        <div className="mx-auto max-w-6xl px-6 py-28 space-y-24">
          {[
            {
              title: "Configure once",
              text: "Define search queries, locations, salary limits, and filters using environment variables.",
            },
            {
              title: "Automated discovery",
              text: "Runs on a schedule, paginates results, and deduplicates aggressively.",
            },
            {
              title: "Clean weekly report",
              text: "Delivered as a readable Markdown report or GitHub Issue.",
            },
          ].map((step, whichGIF) => (
            <div key={whichGIF} className="grid md:grid-cols-2 gap-12 items-center">
              <div>
                <h2 className="text-3xl font-semibold tracking-tight">
                  {step.title}
                </h2>
                <p className="mt-4 text-lg text-white/70">{step.text}</p>
              </div>

              <div className="relative h-56 overflow-hidden rounded-2xl border border-white/10 bg-black">
                <img
                  src={
                    whichGIF === 0 ? configureGIF : whichGIF === 1 ? automatedDiscoveryGIF : weeklyReportGIF
                  }
                  alt={step.title}
                  className="h-full w-full object-cover"
                />
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* TESTIMONIALS */}
      <section className="border-t border-white/10">
        <div className="mx-auto max-w-6xl px-6 py-28">
          <h2 className="text-3xl font-semibold tracking-tight">
            What developers say
          </h2>
          <p className="mt-3 max-w-xl text-white/60">
            Built for people who prefer signal over noise.
          </p>

          <div className="mt-10 relative h-[340px] overflow-hidden rounded-2xl border border-white/10 bg-white/5">
            {/* fade masks */}
            <div className="pointer-events-none absolute top-0 left-0 right-0 h-20 bg-gradient-to-b from-neutral-950 to-transparent z-10" />
            <div className="pointer-events-none absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-neutral-950 to-transparent z-10" />

            <div
              ref={tickerRef}
              className="space-y-4 p-4 will-change-transform"
            >
              {[
                {
                  quote:
                    "Feels like a personal recruiter that just runs quietly.",
                  user: "@Aumtk",
                },
                {
                  quote:
                    "Pagination and dedupe alone saved me hours every week.",
                  user: "@bh4vya",
                },
                {
                  quote: "The GitHub Issue format makes skimming effortless.",
                  user: "@JamesMeta",
                },
                {
                  quote: "No dashboards, no logins, no nonsense.",
                  user: "@Yanny24211",
                },
                {
                  quote: "Docker support made setup trivial.",
                  user: "@deep-patel21",
                },
              ].map((t, i) => (
                <div
                  key={i}
                  className="rounded-xl border border-white/10 bg-white/10 p-4 backdrop-blur"
                >
                  <p className="text-white/90">{t.quote}</p>
                  <p className="mt-2 text-sm text-white/50">{t.user}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="border-t border-white/10">
        <div className="mx-auto max-w-6xl px-6 py-10 flex flex-col md:flex-row justify-between gap-4 text-sm text-white/50">
          <span>Job Finder Automation</span>
          <span>Python · GitHub Actions · Docker</span>
        </div>
      </footer>
    </main>
  );
}
