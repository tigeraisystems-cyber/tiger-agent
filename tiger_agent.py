"""
Tiger V3 - Autonomous Revenue-Generating AI Agent with Product Creation
Ontario, Canada compliant | Zero-cost operations (except API usage)
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import requests
from anthropic import Anthropic
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY


class TigerAgentV3:
    """
    Tiger's complete autonomous engine: Analyze → Decide → Create
    """
    
    def __init__(self):
        self.memory_file = "tiger_memory.json"
        self.memory = self.load_memory()
        self.products_dir = "tiger_products"
        
        # Create products directory if it doesn't exist
        os.makedirs(self.products_dir, exist_ok=True)
        
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
        """Search for trending digital product opportunities"""
        print(f"🔍 Searching for trending digital products...")
        
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
                "keyword": "Budget planner guide for beginners",
                "category": "Finance",
                "search_volume": "medium",
                "competition": "low"
            },
            {
                "keyword": "Social media content calendar templates",
                "category": "Marketing",
                "search_volume": "high",
                "competition": "medium"
            }
        ]
        
        print(f"✅ Found {len(trending_niches)} trending opportunities")
        return trending_niches
    
    def ai_analyze_opportunity(self, trend: Dict) -> Dict:
        """Use Claude AI to analyze if a trend is worth pursuing"""
        print(f"\n🧠 AI analyzing opportunity: {trend['keyword']}")
        
        keyword = trend['keyword']
        
        # Check memory
        if keyword in self.memory["failed_niches"]:
            print(f"❌ Previously failed - skipping")
            return {"decision": "skip", "confidence": 0.0, "trend": keyword}
        
        if keyword in self.memory["successful_niches"]:
            print(f"✅ Previously successful - high priority")
            return {"decision": "create", "confidence": 0.95, "trend": keyword, 
                   "reasoning": "Proven success in our history"}
        
        # Build context
        context = f"""
        Previous successful niches: {', '.join(self.memory['successful_niches'][:3]) or 'None yet'}
        Previous failed niches: {', '.join(self.memory['failed_niches'][:3]) or 'None yet'}
        Total products created: {len(self.memory['products_created'])}
        """
        
        try:
            prompt = f"""You are Tiger, an autonomous revenue-generating AI agent operating in Ontario, Canada.

OPPORTUNITY TO ANALYZE:
- Keyword: {trend['keyword']}
- Category: {trend['category']}
- Search Volume: {trend['search_volume']}
- Competition: {trend['competition']}

YOUR CONTEXT:
{context}

Analyze this opportunity and respond in JSON format:
{{
    "decision": "create" or "monitor" or "skip",
    "confidence": 0.0 to 1.0,
    "reasoning": "Brief strategic explanation",
    "estimated_price_point": "$X.XX",
    "product_type": "guide", "ebook", or "template_collection"
}}

Focus on products we can create as PDFs/ebooks right now."""

            response = self.ai.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            ai_response = response.content[0].text
            
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
            else:
                analysis = {"decision": "monitor", "confidence": 0.5, "reasoning": ai_response[:200]}
            
            analysis["trend"] = keyword
            
            print(f"🎯 AI DECISION: {analysis['decision'].upper()} (confidence: {analysis['confidence']})")
            print(f"💡 Reasoning: {analysis.get('reasoning', 'N/A')[:100]}...")
            
            return analysis
            
        except Exception as e:
            print(f"⚠️ AI analysis error: {e}")
            return {"decision": "monitor", "confidence": 0.5, "trend": keyword}
    
    def ai_create_product_content(self, product_decision: Dict) -> Dict:
        """
        Use Claude AI to generate the actual product content.
        This is where Tiger creates valuable digital products!
        """
        print(f"\n📝 AI generating product content for: {product_decision['trend']}")
        
        try:
            prompt = f"""You are Tiger's product creation engine. Create a complete, valuable digital product.

PRODUCT TO CREATE:
- Topic: {product_decision['trend']}
- Type: PDF Guide/Ebook
- Target Price: {product_decision.get('estimated_price_point', '$9.99')}

REQUIREMENTS:
1. Create a comprehensive, professional guide (2000-3000 words)
2. Include: Introduction, 5-7 main sections, actionable tips, conclusion
3. Make it immediately useful and worth the price
4. Ontario/Canada compliant content
5. Professional tone but accessible

Provide the content in this JSON structure:
{{
    "title": "Product Title",
    "subtitle": "Compelling subtitle",
    "sections": [
        {{
            "heading": "Section 1 Title",
            "content": "Full section content here..."
        }},
        ...
    ],
    "author": "Tiger AI Systems",
    "price": "$9.99"
}}

Make this a genuinely valuable product that people will want to buy!"""

            response = self.ai.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            ai_response = response.content[0].text
            
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                content = json.loads(json_match.group())
                print(f"✅ Product content generated: {content['title']}")
                return content
            else:
                print(f"⚠️ Failed to parse product content")
                return None
            
        except Exception as e:
            print(f"❌ Content generation error: {e}")
            return None
    
    def create_pdf_product(self, content: Dict, output_filename: str) -> str:
        """
        Create a professional PDF product from AI-generated content.
        Uses reportlab to generate high-quality PDFs.
        """
        print(f"🎨 Creating PDF: {output_filename}")
        
        filepath = os.path.join(self.products_dir, output_filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                              topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        # Styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=12,
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#666666'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=20
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        )
        
        # Build story
        story = []
        
        # Title page
        story.append(Spacer(1, 1.5*inch))
        story.append(Paragraph(content['title'], title_style))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(content.get('subtitle', ''), subtitle_style))
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(f"By {content.get('author', 'Tiger AI Systems')}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(f"© {datetime.now().year} Tiger AI Systems", styles['Normal']))
        story.append(PageBreak())
        
        # Content sections
        for section in content.get('sections', []):
            story.append(Paragraph(section['heading'], heading_style))
            
            # Split content into paragraphs
            paragraphs = section['content'].split('\n\n')
            for para in paragraphs:
                if para.strip():
                    story.append(Paragraph(para.strip(), body_style))
                    story.append(Spacer(1, 0.1*inch))
        
        # Build PDF
        doc.build(story)
        
        print(f"✅ PDF created: {filepath}")
        return filepath
    
    def log_decision(self, analysis: Dict):
        """Log Tiger's decision to memory"""
        decision_record = {
            "timestamp": datetime.now().isoformat(),
            "trend": analysis["trend"],
            "decision": analysis["decision"],
            "confidence": analysis.get("confidence", 0.5),
            "reasoning": analysis.get("reasoning", "No reasoning provided"),
            "ai_powered": True
        }
        
        if "estimated_price_point" in analysis:
            decision_record["estimated_price"] = analysis["estimated_price_point"]
        
        self.memory["decisions"].append(decision_record)
        self.save_memory()
    
    def log_product_creation(self, product_info: Dict):
        """Log created product to memory"""
        self.memory["products_created"].append(product_info)
        self.save_memory()
    
    def run_cycle(self):
        """
        Tiger's complete autonomous loop: Analyze → Decide → Create
        """
        print("=" * 60)
        print("🐯 TIGER AGENT V3 - AUTONOMOUS PRODUCT CREATION")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Step 1: Search trends
        trends = self.search_trends()
        
        if not trends:
            print("⚠️ No trends found")
            return self.memory
        
        # Step 2: AI analysis
        print(f"\n🤖 AI analyzing top opportunities...")
        
        products_to_create = []
        
        for trend in trends[:2]:  # Limit to 2 per cycle to control costs
            analysis = self.ai_analyze_opportunity(trend)
            self.log_decision(analysis)
            
            if analysis["decision"] == "create" and analysis.get("confidence", 0) >= 0.75:
                products_to_create.append(analysis)
        
        # Step 3: Product Creation
        if products_to_create:
            print(f"\n🏭 CREATING {len(products_to_create)} PRODUCTS...")
            
            for decision in products_to_create:
                print(f"\n{'='*60}")
                
                # Generate content with AI
                content = self.ai_create_product_content(decision)
                
                if content:
                    # Create PDF
                    filename = f"{decision['trend'][:50].replace(' ', '_').replace('/', '_')}.pdf"
                    filepath = self.create_pdf_product(content, filename)
                    
                    # Log product
                    product_info = {
                        "timestamp": datetime.now().isoformat(),
                        "trend": decision['trend'],
                        "filename": filename,
                        "filepath": filepath,
                        "title": content['title'],
                        "estimated_price": decision.get('estimated_price_point', '$9.99'),
                        "status": "created"
                    }
                    self.log_product_creation(product_info)
                    
                    print(f"✅ PRODUCT CREATED: {content['title']}")
                else:
                    print(f"❌ Failed to create product for: {decision['trend']}")
        
        # Step 4: Summary
        print("\n" + "=" * 60)
        print("📈 CYCLE SUMMARY")
        print(f"Total decisions made: {len(self.memory['decisions'])}")
        print(f"Products created this cycle: {len(products_to_create)}")
        print(f"Total products in catalog: {len(self.memory['products_created'])}")
        
        if self.memory['products_created']:
            print(f"\n📦 LATEST PRODUCTS:")
            for product in self.memory['products_created'][-3:]:
                print(f"  - {product['title']} ({product['estimated_price']})")
        
        print("=" * 60)
        
        return self.memory


def main():
    """Entry point for GitHub Actions"""
    try:
        tiger = TigerAgentV3()
        tiger.run_cycle()
    except Exception as e:
        print(f"❌ Tiger encountered an error: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
