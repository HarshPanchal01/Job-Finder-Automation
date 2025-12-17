import { useEffect, useRef, useState } from "react";
import logo from "./assets/automationLogo.png";
import configureGIF from "./assets/ConfigureAnimation.gif";
import weeklyReportGIF from "./assets/CleanWeeklyReportAnimation.gif";
import automatedDiscoveryGIF from "./assets/AutomatedDiscoveryAnimation.gif";
import pythonLogo from "./assets/python-logo-only.png";
import serpapiLogo from "./assets/serpapi-logo.png";
import githubLogo from "./assets/github-mark-white.png";
import dockerLogo from "./assets/docker-mark-blue.png";
import secretsImage from "./assets/secrets.png";
import variablesImage from "./assets/variables.png";
import actionsImage from "./assets/actions-logs.png";
import jobHistoryImage from "./assets/job-history.png";
import emailInboxImage from "./assets/email-inbox.png";
import githubIssueImage from "./assets/github-issue.png";

type Theme = "light" | "dark";
const STORAGE_KEY = "jfa_theme";

export default function App() {
  const tickerRef = useRef<HTMLDivElement | null>(null);

  // Theme state
  const [theme, setTheme] = useState<Theme>("dark");
  const isDark = theme === "dark";

  const applyTheme = (t: Theme) => {
    document.documentElement.classList.toggle("dark", t === "dark");
  };

  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY) as Theme | null;
    const system: Theme = window.matchMedia?.("(prefers-color-scheme: dark)")
      .matches
      ? "dark"
      : "light";
    const initial = saved ?? system;

    setTheme(initial);
    applyTheme(initial);
  }, []);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, theme);
    applyTheme(theme);
  }, [theme]);

  const toggleTheme = () => setTheme((t) => (t === "dark" ? "light" : "dark"));

  // Testimonials ticker
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

  const [expandedImage, setExpandedImage] = useState<string | null>(null);

  return (
    <main className="min-h-screen bg-white text-neutral-950 antialiased dark:bg-neutral-950 dark:text-white">
      {/* HEADER */}
      <header className="sticky top-0 z-50 border-b border-black/10 bg-white/70 backdrop-blur dark:border-white/10 dark:bg-neutral-950/70">
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
              className="text-neutral-700 hover:text-neutral-950 transition dark:text-white/70 dark:hover:text-white"
            >
              How it works
            </a>
            <a
              href="https://github.com/HarshPanchal01/Job-Finder-Automation"
              target="_blank"
              rel="noreferrer"
              className="rounded-lg border border-black/15 px-4 py-2 text-neutral-700 hover:border-black/30 transition dark:border-white/15 dark:text-white/80 dark:hover:border-white/30"
            >
              GitHub
            </a>

            <button
              type="button"
              onClick={toggleTheme}
              aria-label={
                isDark ? "Switch to light mode" : "Switch to dark mode"
              }
              className="rounded-lg border border-black/15 px-3 py-2 text-neutral-700 hover:border-black/30 transition dark:border-white/15 dark:text-white/80 dark:hover:border-white/30"
              title={isDark ? "Light mode" : "Dark mode"}
            >
              {isDark ? "☀️" : "🌙"}
            </button>
          </nav>
        </div>
      </header>

      {/* HERO */}
      <section className="relative overflow-hidden">
        <div className="mx-auto max-w-6xl px-6 py-32">
          <h1 className="text-5xl md:text-6xl font-semibold tracking-tight leading-tight">
            Job searching,
            <br />
            <span className="text-yellow-700/90 dark:text-yellow-200/80">
              without the noise.
            </span>
          </h1>

          <p className="mt-6 max-w-xl text-lg text-neutral-700 dark:text-white/70">
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
              className="rounded-xl border border-black/20 px-6 py-3 text-neutral-800 hover:border-black/40 transition dark:border-white/20 dark:text-white/80 dark:hover:border-white/40"
            >
              View on GitHub
            </a>
          </div>
        </div>

        <div className="absolute inset-0 -z-10 bg-gradient-to-b from-yellow-400/15 via-transparent to-transparent" />
      </section>

      {/* HOW IT WORKS */}
      <section
        id="how"
        className="border-t border-black/10 dark:border-white/10"
      >
        <div className="mx-auto max-w-6xl px-6 py-28 space-y-20">
          {[
            {
              title: "Configure once",
              text: "Define search queries, locations, salary limits, and filters using environment variables.",
              gif: configureGIF,
              alt: "Config setup demo",
            },
            {
              title: "Automated discovery",
              text: "Runs on a schedule, paginates results, and deduplicates aggressively.",
              gif: automatedDiscoveryGIF,
              alt: "Pagination and dedupe demo",
            },
            {
              title: "Clean weekly report",
              text: "Delivered as email, GitHub issue, and markdown report.",
              gif: weeklyReportGIF,
              alt: "Report output demo",
            },
          ].map((step, i) => (
            <div key={i} className="space-y-6">
              <div>
                <h2 className="text-3xl font-semibold tracking-tight">
                  {step.title}
                </h2>
                <p className="mt-4 max-w-3xl text-lg text-neutral-700 dark:text-white/70">
                  {step.text}
                </p>
              </div>

              <div className="overflow-hidden rounded-2xl border border-black/10 bg-black/5 dark:border-white/10 dark:bg-white/5">
                <img
                  src={step.gif}
                  alt={step.alt}
                  className="w-full h-auto object-contain"
                  loading="lazy"
                />
              </div>

              {i === 0 && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
                  <div
                    onClick={() => setExpandedImage(secretsImage)}
                    className="overflow-hidden rounded-2xl border border-black/10 bg-black/5 p-4 cursor-pointer hover:border-black/30 hover:bg-black/10 transition-all hover:scale-105 flex flex-col dark:border-white/10 dark:bg-white/5 dark:hover:border-white/30 dark:hover:bg-white/10"
                  >
                    <p className="text-sm font-medium text-neutral-700 dark:text-white/70 mb-3">
                      Add GitHub secrets (Click to expand)
                    </p>
                    <div className="h-[240px] md:h-[260px] flex items-center justify-center">
                      <img
                        src={secretsImage}
                        alt="GitHub Secrets setup"
                        className="w-full max-h-full object-contain"
                        loading="lazy"
                      />
                    </div>
                  </div>

                  <div
                    onClick={() => setExpandedImage(variablesImage)}
                    className="overflow-hidden rounded-2xl border border-black/10 bg-black/5 p-4 cursor-pointer hover:border-black/30 hover:bg-black/10 transition-all hover:scale-105 flex flex-col dark:border-white/10 dark:bg-white/5 dark:hover:border-white/30 dark:hover:bg-white/10"
                  >
                    <p className="text-sm font-medium text-neutral-700 dark:text-white/70 mb-3">
                      Add GitHub variables (Click to expand)
                    </p>
                    <div className="h-[240px] md:h-[260px] flex items-center justify-center">
                      <img
                        src={variablesImage}
                        alt="GitHub Variables setup"
                        className="w-full max-h-full object-contain"
                        loading="lazy"
                      />
                    </div>
                  </div>
                </div>
              )}

              {i === 1 && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
                  <div
                    onClick={() => setExpandedImage(actionsImage)}
                    className="overflow-hidden rounded-2xl border border-black/10 bg-black/5 p-4 cursor-pointer hover:border-black/30 hover:bg-black/10 transition-all hover:scale-105 flex flex-col dark:border-white/10 dark:bg-white/5 dark:hover:border-white/30 dark:hover:bg-white/10"
                  >
                    <p className="text-sm font-medium text-neutral-700 dark:text-white/70 mb-3">
                      Filtering logs (Click to expand)
                    </p>
                    <div className="h-[240px] md:h-[260px] flex items-center justify-center">
                      <img
                        src={actionsImage}
                        alt="Automated discovery screenshot 1"
                        className="w-full max-h-full object-contain"
                        loading="lazy"
                      />
                    </div>
                  </div>

                  <div
                    onClick={() => setExpandedImage(jobHistoryImage)}
                    className="overflow-hidden rounded-2xl border border-black/10 bg-black/5 p-4 cursor-pointer hover:border-black/30 hover:bg-black/10 transition-all hover:scale-105 flex flex-col dark:border-white/10 dark:bg-white/5 dark:hover:border-white/30 dark:hover:bg-white/10"
                  >
                    <p className="text-sm font-medium text-neutral-700 dark:text-white/70 mb-3">
                      Job history for deduplication in subsequent runs (Click to
                      expand)
                    </p>
                    <div className="h-[240px] md:h-[260px] flex items-center justify-center">
                      <img
                        src={jobHistoryImage}
                        alt="Automated discovery screenshot 2"
                        className="w-full max-h-full object-contain"
                        loading="lazy"
                      />
                    </div>
                  </div>
                </div>
              )}

              {i === 2 && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
                  <div
                    onClick={() => setExpandedImage(emailInboxImage)}
                    className="overflow-hidden rounded-2xl border border-black/10 bg-black/5 p-4 cursor-pointer hover:border-black/30 hover:bg-black/10 transition-all hover:scale-105 flex flex-col dark:border-white/10 dark:bg-white/5 dark:hover:border-white/30 dark:hover:bg-white/10"
                  >
                    <p className="text-sm font-medium text-neutral-700 dark:text-white/70 mb-3">
                      Delivered to your email inbox (Click to expand)
                    </p>
                    <div className="h-[240px] md:h-[260px] flex items-center justify-center">
                      <img
                        src={emailInboxImage}
                        alt="Email inbox with weekly report"
                        className="w-full max-h-full object-contain"
                        loading="lazy"
                      />
                    </div>
                  </div>

                  <div
                    onClick={() => setExpandedImage(githubIssueImage)}
                    className="overflow-hidden rounded-2xl border border-black/10 bg-black/5 p-4 cursor-pointer hover:border-black/30 hover:bg-black/10 transition-all hover:scale-105 flex flex-col dark:border-white/10 dark:bg-white/5 dark:hover:border-white/30 dark:hover:bg-white/10"
                  >
                    <p className="text-sm font-medium text-neutral-700 dark:text-white/70 mb-3">
                      Delivered as a GitHub issue (Click to expand)
                    </p>
                    <div className="h-[240px] md:h-[260px] flex items-center justify-center">
                      <img
                        src={githubIssueImage}
                        alt="GitHub Issue with weekly report"
                        className="w-full max-h-full object-contain"
                        loading="lazy"
                      />
                    </div>
                  </div>
                </div>
              )}

              {i !== 2 && (
                <div className="border-t border-black/10 pt-2 dark:border-white/10" />
              )}
            </div>
          ))}
        </div>
      </section>

      {/* TESTIMONIALS */}
      <section className="border-t border-black/10 dark:border-white/10">
        <div className="mx-auto max-w-6xl px-6 py-28">
          <h2 className="text-3xl font-semibold tracking-tight">
            What developers say
          </h2>
          <p className="mt-3 max-w-xl text-lg text-neutral-700 dark:text-white/70">
            Built for people who prefer simple efficient solutions.
          </p>

          <div className="mt-10 relative h-[340px] overflow-hidden rounded-2xl border border-black/10 bg-black/5 dark:border-white/10 dark:bg-white/5">
            {/* fade masks */}
            <div className="pointer-events-none absolute top-0 left-0 right-0 h-20 bg-gradient-to-b from-white to-transparent z-10 dark:from-neutral-950" />
            <div className="pointer-events-none absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-white to-transparent z-10 dark:from-neutral-950" />

            <div
              ref={tickerRef}
              className="space-y-4 p-4 will-change-transform"
            >
              {[
                {
                  quote: "Feels like a job notifier that actually works.",
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
                  className="rounded-xl border border-black/10 bg-black/10 p-4 backdrop-blur dark:border-white/10 dark:bg-white/10"
                >
                  <p className="text-lg text-neutral-900 dark:text-white/90">
                    {t.quote}
                  </p>
                  <p className="mt-2 text-sm text-neutral-500 dark:text-white/50">
                    {t.user}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="border-t border-black/10 dark:border-white/10">
        <div className="mx-auto max-w-6xl px-6 py-12">
          <div className="flex flex-col items-center justify-center gap-8">
            <button
              onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
              className="text-lg font-semibold text-neutral-700 hover:text-neutral-950 transition dark:text-white/70 dark:hover:text-white"
            >
              Job Finder Automation
            </button>

            <div className="flex justify-center items-center gap-12">
              <div className="flex flex-col items-center gap-2">
                <div className="w-12 h-12 flex items-center justify-center">
                  <img
                    src={pythonLogo}
                    alt="Python"
                    className="max-w-full max-h-full object-contain"
                  />
                </div>
                <span className="text-sm font-medium text-neutral-700 dark:text-white/70">
                  Python
                </span>
              </div>

              <div className="flex flex-col items-center gap-2">
                <div className="w-12 h-12 flex items-center justify-center">
                  <img
                    src={serpapiLogo}
                    alt="SerpAPI"
                    className="max-w-full max-h-full object-contain"
                  />
                </div>
                <span className="text-sm font-medium text-neutral-700 dark:text-white/70">
                  SerpApi
                </span>
              </div>

              <div className="flex flex-col items-center gap-2">
                <div className="w-12 h-12 flex items-center justify-center">
                  <img
                    src={githubLogo}
                    alt="GitHub"
                    className="max-w-full max-h-full object-contain"
                  />
                </div>
                <span className="text-sm font-medium text-neutral-700 dark:text-white/70">
                  GitHub
                </span>
              </div>

              <div className="flex flex-col items-center gap-2">
                <div className="w-12 h-12 flex items-center justify-center">
                  <img
                    src={dockerLogo}
                    alt="Docker"
                    className="max-w-full max-h-full object-contain"
                  />
                </div>
                <span className="text-sm font-medium text-neutral-700 dark:text-white/70">
                  Docker
                </span>
              </div>
            </div>

            <p className="mt-6 text-sm text-neutral-600 flex flex-wrap items-center gap-1 dark:text-white/60">
              <span className="ml-2">© 2025</span>
              <span>Made with care by</span>
              <a
                href="https://github.com/HarshPanchal01"
                target="_blank"
                rel="noreferrer"
                className="underline underline-offset-4 hover:text-neutral-950 dark:hover:text-white"
              >
                Harsh
              </a>
              <span>&amp;</span>
              <a
                href="https://github.com/anmolp476"
                target="_blank"
                rel="noreferrer"
                className="underline underline-offset-4 hover:text-neutral-950 dark:hover:text-white"
              >
                Anmol
              </a>
            </p>
          </div>
        </div>
      </footer>

      {/* Image Modal */}
      {expandedImage && (
        <div
          className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/80 backdrop-blur p-4"
          onClick={() => setExpandedImage(null)}
        >
          <div
            className="relative w-[80vw] h-[80vh] flex items-center justify-center"
            onClick={(e) => e.stopPropagation()}
          >
            <img
              src={expandedImage}
              alt="Expanded view"
              className="max-w-full max-h-full object-contain rounded-lg"
            />
            <button
              onClick={() => setExpandedImage(null)}
              className="absolute -top-10 -right-10 bg-white/20 hover:bg-white/40 text-white rounded-full w-10 h-10 flex items-center justify-center transition-colors"
              aria-label="Close"
            >
              ✕
            </button>
          </div>
        </div>
      )}
    </main>
  );
}
