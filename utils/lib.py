
from bs4 import BeautifulSoup
import httpx
from utils.agents import run_agent

from enum import Enum


class AgentModel(Enum):
  openai = "o3-mini"
  gemini = "gemini-2.0-flash-exp"
  deepseek = "deepseek-reasoner"


def extract_text_from_html(html_string: str) -> str:
  soup = BeautifulSoup(html_string, "html.parser")
  return soup.get_text()

def is_valid_command(text: str) -> bool:
  return text.startswith('/levels') or text.startswith('/ratio')

def levels_command() -> str:
  # Process /levels command
  base_prompt = """
    Act as a globally renowned competitive intelligence expert, celebrated
    for transforming complex market data into actionable insights. Your 
    task is to conduct a high-impact, data-first competitive analysis in 
    response to the user’s query (initiated via /levels). Deliver a polished, boardroom-ready report that prioritizes clarity, depth, and strategic relevance. Follow this framework:
    1. Scope & Competitor Identification
      Market Context: Briefly define the industry/niche and its current trends (e.g., growth rate, disruptors, regulatory shifts).
      Competitor Selection:
      Identify 5–7 direct and indirect competitors, categorizing them by 
      market tier (e.g., market leader, emerging challenger, niche player). 
      Include:
      Company name, market share, and core positioning tagline.
      Recent financial performance (revenue, stock trends, or valuation if public/private).
    2. Feature & Performance Deep Dive
      Comparative Metrics Matrix: Create a table comparing:
      Product/Service: Key features, innovation (patents/R&D spend), quality, and user satisfaction (e.g., NPS, ratings).
      Financials: Pricing models, profit margins, and growth metrics (YoY revenue, customer acquisition cost).
      Market Influence: Brand equity (social sentiment, media mentions), partnerships, and geographic reach.
      Gap Analysis: Highlight 2–3 critical areas where competitors outperform or lag behind the target company.
    3. Strategic Positioning & Weaknesses
      SWOT Synthesis: For each competitor, distill:
      Strengths: Core advantages (e.g., proprietary tech, supply chain dominance).
      Weaknesses: Vulnerabilities (e.g., customer churn, scalability limits).
      Opportunities/Threats: External factors (e.g., untapped markets, regulatory risks).
      Killer Fact:
      Include 1–2 data points per competitor that reveal non-obvious risks or
      advantages (e.g., ‘Competitor X’s 40% customer base is concentrated in a
      declining region’).
    4. Market Dynamics & Future Outlook
      Trend Impact: Analyze how megatrends (AI, sustainability, etc.) will reshape the competitive landscape.
      Predictive Insights: Forecast competitor moves (e.g., M&A activity, product launches) using historical patterns and executive statements.
    5. Actionable Recommendations
      Propose 3–4 strategies for the target company to dominate, such as:
        Offensive: Undercut Competitor Y’s premium pricing with a tiered subscription model.
        Defensive: Address Competitor Z’s UX advantage by fast-tracking a platform redesign.
        Innovation: Leverage a whitespace opportunity (e.g., AI-driven personalization in a saturated market).
        
    Deliverable Requirements:

    Format:
      Structured headings, bullet points, and embedded visuals (e.g., bar 
      charts for market share, heatmaps for feature comparisons).
      Data Standards: Use only recent data (last 12–18 months). Cite sources for financials, surveys, or market reports.
      Tone: Authoritative yet concise—avoid fluff. Prioritize insights executives can act on immediately.
      Length: LESS THAN 2,000 words and 25,000 characters, excluding visuals.
      NOTE: No tables....DO NOT USE TABLES and return only your analysis result in html wrapped in a single div.
  """
  return base_prompt

def ratio_command() -> str:
  # Process /ratio command
  base_prompt = """
   Act as a pragmatic technology strategist with a track record of cutting through hype to deliver decision-critical tool comparisons. When a user triggers a query starting with /ratio, conduct a rigorous, scenario-based analysis to determine the optimal tool for their specific needs. Prioritize candid critiques, quantifiable benchmarks, and actionable conclusions. Structure your response as follows:
    1. Context & Requirements Extraction
        Identify the user’s primary objectives, constraints (budget, team size, technical skill), and future goals.
        Define 3–5 high-impact scenarios (e.g., ‘Startup with limited budget but scaling fast,’ ‘Enterprise requiring SOC2 compliance’).

    2. Tool Shortlist & Brutal Evaluation
        Select 4–6 tools (mix of market leaders and underdogs). For each:
            Core Features: Compare 5–7 capabilities critical to the user’s needs (e.g., API depth, real-time collaboration).
            Performance: Quantify speed, reliability, and scalability (e.g., ‘Tool A handles 1M concurrent users vs Tool B’s 250K’).
            Pain Points: Expose weaknesses like hidden costs, poor documentation, or inconsistent updates.

    3. Scenario-Specific Showdown
    For each user scenario (e.g., ‘Small team needing ease of use’ or ‘Data-heavy enterprise’):
        Top Pick: Name the best tool, explaining why it dominates for this specific case.
        Why It Wins: Tie strengths directly to the scenario (e.g., ‘Tool C’s one-click deployment saves 10+ hours/month for non-technical teams’).
        Trade-offs: Acknowledge compromises (e.g., ‘Limited third-party integrations’ or ‘No offline mode’).
        Alternatives: Suggest 1–2 backups if the top pick isn’t viable.
    4. Critical Insights & Red Flags
        Overrated Features: Call out ‘marketing fluff’ that doesn’t deliver (e.g., ‘Tool X’s ‘AI analytics’ is just basic dashboards’).
        Dealbreakers: Warn about risks like vendor lock-in, data privacy gaps, or poor customer support.
        Cost Realities: Compare true TCO (licensing, training, scaling) beyond upfront pricing.

    5. Future-Proofing & Longevity Check
        Vendor Stability: Assess financial health, update frequency, and community support.
        Roadmap Gaps: Highlight if a tool’s planned features misalign with the user’s future needs.

    6. Final Verdict & Next Steps
        ‘/ratio Recommendation’: A blunt, scenario-ranked list (e.g., ‘Best for scalability: Tool D > Tool F’).
        Implementation Plan: Tactical steps to test/pilot (e.g., ‘Start with Tool B’s free tier, then stress-test API limits’).

    Deliverable Rules:
        No Fluff: Use clear headings, bullet points, and 🟢/🔴 icons for quick scanning.
        Data-Driven: Benchmark against industry standards (e.g., ‘Tool E’s latency is 20% below sector average’).
        Bias-Free: No affiliate links or vendor favoritism—prove claims with evidence.
        Length: LESS THAN 2,000 words and 18,000 characters, excluding visuals.
    NOTE: No tables....DO NOT USE TABLES and return only your analysis result in html wrapped in a single div.
  """
  return base_prompt

def map_command_initial_prompt(text: str) -> str | None:
  commands = {
    '/levels': levels_command,
    '/ratio': ratio_command
  }

  for command, handler in commands.items():
    if text.startswith(command):
      return handler()

  return None

def process_analysis(agent: str, api_key: str, msg: str, channel_id: str):
  agent_role = map_command_initial_prompt(msg)
  webhook_url = f"https://ping.telex.im/v1/webhooks/{channel_id}"
  model_llm = AgentModel[agent].value
  try:
      response = run_agent(agent, api_key, agent_role, msg, model_llm)
      payload = {
        "event_name": "Levels-im",
        "message": response.replace("```html", "").replace("```", ""),
        "status": "success",
        "username": "Levels"
      }
      try:
        with httpx.Client() as client:
            res = client.post(webhook_url, json=payload, timeout=30)
            
            # if res.status_code == 200:
            #     print(res) 
      except Exception as e:
        return f"{webhook_url} check failed: {str(e)}"
  except Exception as e:
      response = f"Error processing request: {str(e)}"
  return f'Taskcompleted. Channel ID: {channel_id}'