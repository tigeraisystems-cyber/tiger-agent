"""
Tiger V2 - Autonomous Revenue-Generating AI Agent with AI Decision-Making
Ontario, Canada compliant | Zero-cost operations (except API usage)
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import requests
from anthropic import Anthropic


class TigerAgentV2:
    """
    Tiger's upgraded decision-making engine with AI-powered analysis.
    """
    
    def __init__(self):
        self.memory_file = "tiger_memory.json"
        self.memory = self.load_memory()
        
        # Initialize Claude AI
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        self.ai = Anthropic(api_key=api_key)
        
    def load_memory(self) -> Dict:
        """Load Tiger's memory from JSON file"""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return {
            "decisions": [],
            "products_created": [],
            "successful_niches": [],
            "failed_niches": [],
            "total_revenue": 0,
            "learnings": []
        }
    
    def save_memory(self):
        """Save Tiger's memory to JSON file"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, indent=2, fp=f)
    
    def search_trends(self) -> List[Dict]:
        """
        Search for trending digital product opportunities.
        Uses multiple free sources to identify trends.
        """
        print(f"🔍 Searching for trending digital products...")
        
        trends = []
        
        # Method 1: Search trending topics via free news API
        try:
            # Using a simple approach - searching for digital product trends
            search_queries = [
                "digital product trends 2025",
                "best selling templates online",
                "profitable digital downloads"
            ]
            
            # For now, we'll use curated high-potential niches
            # In production, you'd integrate Google Trends API or similar
            trending_niches = [
                {
                    "keyword": "AI prompt templates for ChatGPT",
                    "category": "AI Tools",
                    "search_volume": "high",
                    "competition": "medium"
                },
                {
                    "keyword": "Notion dashboard templates for productivity",
                    "category": "Productivity",
                    "search_volume": "high",
                    "competition": "medium"
                },
                {
                    "keyword": "Resume templates ATS-friendly 2025",
                    "category": "Career",
                    "search_volume": "very high",
                    "competition": "high"
                },
                {
                    "keyword": "Instagram Reels templates for businesses",
                    "category": "Social Media",
                    "search_volume": "high",
                    "competition": "medium"
                },
                {
                    "keyword": "Budget planner spreadsheet templates",
                    "category": "Finance",
                    "search_volume": "medium",
                    "competition": "low"
                }
            ]
            
            trends = trending_niches
            print(f"✅ Found {len(trends)} trending opportunities")
            
        except Exception as e:
            print(f"⚠️ Error searching trends: {e}")
            trends = []
        
        return trends
    
    def ai_analyze_opportunity(self, trend: Dict) -> Dict:
        """
        Use Claude AI to deeply analyze if a trend is worth pursuing.
        This is Tiger's real intelligence - AI-powered market analysis.
        """
        print(f"\n🧠 AI analyzing opportunity: {trend['keyword']}")
        
        # Check memory - have we tried this before?
        keyword = trend['keyword']
        if keyword in self.memory["failed_niches"]:
            print(f"❌ Previously failed - skipping AI analysis")
            return {
                "decision": "skip",
                "reason": "Previously failed niche",
                "confidence": 0.0,
                "trend": keyword
            }
        
        if keyword in self.memory["successful_niches"]:
            print(f"✅ Previously successful - high priority")
            return {
                "decision": "create",
                "reason": "Proven success in our history",
                "confidence": 0.95,
                "trend": keyword
            }
        
        # Build context from memory
        context = f"""
        Previous successful niches: {', '.join(self.memory['successful_niches'][:3]) or 'None yet'}
        Previous failed niches: {', '.join(self.memory['failed_niches'][:3]) or 'None yet'}
        Total products created: {len(self.memory['products_created'])}
        Total revenue: ${self.memory['total_revenue']}
        """
        
        # Ask Claude to analyze the opportunity
        try:
            prompt = f"""You are Tiger, an autonomous revenue-generating AI agent operating in Ontario, Canada.

Your mission: Analyze digital product opportunities and decide if they're worth pursuing.

OPPORTUNITY TO ANALYZE:
- Keyword: {trend['keyword']}
- Category: {trend['category']}
- Search Volume: {trend['search_volume']}
- Competition: {trend['competition']}

YOUR CONTEXT:
{context}

ANALYSIS CRITERIA:
1. Market Demand: Is there real demand for this?
2. Creation Feasibility: Can this be created with AI/automation?
3. Differentiation: Can we stand out in this niche?
4. Monetization: Can this generate revenue quickly?
5. Legal Compliance: Is this Ontario/Canada compliant?

Provide your analysis in this JSON format:
{{
    "decision": "create" or "monitor" or "skip",
    "confidence": 0.0 to 1.0,
    "reasoning": "Brief explanation of your decision",
    "estimated_creation_time": "e.g., 2 hours",
    "estimated_price_point": "e.g., $9.99",
    "key_differentiator": "What would make our product unique",
    "risks": "Main concerns or risks"
}}

Be strategic, analytical, and focused on revenue generation."""

            response = self.ai.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse AI response
            ai_response = response.content[0].text
            
            # Extract JSON from response (AI might wrap it in markdown)
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
            else:
                # Fallback if JSON parsing fails
                analysis = {
                    "decision": "monitor",
                    "confidence": 0.5,
                    "reasoning": ai_response[:200]
                }
            
            # Add the trend keyword to the analysis
            analysis["trend"] = keyword
            analysis["ai_analysis"] = ai_response
            
            print(f"🎯 AI DECISION: {analysis['decision'].upper()} (confidence: {analysis['confidence']})")
            print(f"💡 Reasoning: {analysis.get('reasoning', 'N/A')[:100]}...")
            
            return analysis
            
        except Exception as e:
            print(f"⚠️ AI analysis error: {e}")
            # Fallback to simple scoring
            return {
                "decision": "monitor",
                "confidence": 0.5,
                "reason": f"AI analysis failed: {str(e)}",
                "trend": keyword
            }
    
    def log_decision(self, analysis: Dict):
        """Log Tiger's AI-powered decision to memory"""
        decision_record = {
            "timestamp": datetime.now().isoformat(),
            "trend": analysis["trend"],
            "decision": analysis["decision"],
            "confidence": analysis.get("confidence", 0.5),
            "reasoning": analysis.get("reasoning", analysis.get("reason", "No reasoning provided")),
            "ai_powered": True
        }
        
        # Add additional AI insights if available
        if "estimated_price_point" in analysis:
            decision_record["estimated_price"] = analysis["estimated_price_point"]
        if "key_differentiator" in analysis:
            decision_record["differentiator"] = analysis["key_differentiator"]
        
        self.memory["decisions"].append(decision_record)
        self.save_memory()
        print(f"💾 Decision logged to memory")
    
    def run_cycle(self):
        """
        Tiger's main autonomous loop with AI decision-making.
        This runs every 6 hours via GitHub Actions.
        """
        print("=" * 60)
        print("🐯 TIGER AGENT V2 - AI-POWERED AUTONOMOUS CYCLE")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Step 1: Search for trending opportunities
        trends = self.search_trends()
        
        if not trends:
            print("⚠️ No trends found this cycle")
            return self.memory
        
        # Step 2: AI-powered analysis of top opportunities
        print(f"\n🤖 AI analyzing top {min(3, len(trends))} opportunities...")
        
        decisions_to_create = []
        
        for trend in trends[:3]:  # Analyze top 3 to control API costs
            analysis = self.ai_analyze_opportunity(trend)
            self.log_decision(analysis)
            
            if analysis["decision"] == "create" and analysis.get("confidence", 0) >= 0.7:
                decisions_to_create.append(analysis)
        
        # Step 3: Summary
        print("\n" + "=" * 60)
        print("📈 CYCLE SUMMARY")
        print(f"Total decisions in history: {len(self.memory['decisions'])}")
        print(f"Products to create this cycle: {len(decisions_to_create)}")
        if decisions_to_create:
            print(f"\n🎯 HIGH-PRIORITY PRODUCTS:")
            for decision in decisions_to_create:
                print(f"  - {decision['trend']} (confidence: {decision['confidence']})")
        print("=" * 60)
        
        return self.memory


def main():
    """Entry point for GitHub Actions"""
    try:
        tiger = TigerAgentV2()
        tiger.run_cycle()
    except Exception as e:
        print(f"❌ Tiger encountered an error: {e}")
        raise


if __name__ == "__main__":
    main()
