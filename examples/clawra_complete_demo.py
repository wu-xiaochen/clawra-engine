"""
Clawra Complete Demo - Full Featured Agent
===========================================

Features:
1. Interactive knowledge graph visualization with PyVis
2. Deep coverage assessment with entity/relation/predicate analysis
3. Enhanced reasoning with forward chaining
4. Real LLM integration for extraction and QA
"""
import streamlit as st
import os
import sys
import json
import asyncio
import time
import hashlib
from typing import List, Dict, Any, Set
from openai import AsyncOpenAI

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from core.reasoner import Reasoner, Fact, Rule
from core.ontology.rule_engine import RuleEngine

# Page Config
st.set_page_config(
    page_title="Clawra Complete | Knowledge Graph & Reasoning",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
<style>
    .stApp { background: #f8fafc; }
    .metric-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .triple-card {
        background: #dcfce7;
        border: 1px solid #86efac;
        border-radius: 6px;
        padding: 8px 12px;
        margin: 4px 0;
    }
    .coverage-high { color: #22c55e; font-weight: bold; }
    .coverage-medium { color: #f59e0b; font-weight: bold; }
    .coverage-low { color: #ef4444; font-weight: bold; }
    .reasoning-chain {
        background: #e0e7ff;
        border-left: 4px solid #6366f1;
        padding: 12px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
    }
</style>
""", unsafe_allow_html=True)


# =========================================
# LLM Client
# =========================================
class LLMClient:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY", "e2e894dc-4ce5-4a7e-87d5-a7da2c12135a"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
        )
        self.model = os.getenv("OPENAI_MODEL", "doubao-seed-2-0-pro-260215")
    
    async def chat(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 2000) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def extract_knowledge(self, text: str) -> List[Dict]:
        prompt = f"""Extract ALL knowledge triples (subject, predicate, object) from the text.
Be comprehensive - extract every piece of information.

Return JSON array:
[{{"subject": "...", "predicate": "...", "object": "...", "confidence": 0.9}}]

Text: {text}

JSON:"""
        
        response = await self.chat([
            {"role": "system", "content": "Extract all knowledge triples comprehensively."},
            {"role": "user", "content": prompt}
        ], temperature=0.3)
        
        try:
            start = response.find('[')
            end = response.rfind(']') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        return []
    
    async def answer_with_reasoning(self, question: str, facts: List[str]) -> Dict:
        """Answer with explicit reasoning steps"""
        facts_text = "\n".join([f"- {f}" for f in facts[:15]])
        
        prompt = f"""Answer the question using the provided facts. Show your reasoning step by step.

Facts:
{facts_text}

Question: {question}

Return JSON:
{{
  "reasoning_steps": ["step1", "step2", ...],
  "answer": "final answer",
  "confidence": 0.85
}}

JSON:"""
        
        response = await self.chat([
            {"role": "system", "content": "Answer with explicit reasoning steps."},
            {"role": "user", "content": prompt}
        ], temperature=0.5)
        
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        
        return {
            "reasoning_steps": ["Direct answer based on facts"],
            "answer": response[:500],
            "confidence": 0.7
        }


# =========================================
# Deep Coverage Assessor
# =========================================
class CoverageAssessor:
    """Deep assessment of knowledge coverage"""
    
    def __init__(self, reasoner: Reasoner):
        self.reasoner = reasoner
    
    def assess(self, new_triples: List[Dict]) -> Dict:
        """Comprehensive coverage assessment"""
        
        # 1. Entity coverage
        existing_entities = self._get_all_entities()
        new_entities = set()
        for t in new_triples:
            new_entities.add(t.get('subject', ''))
            new_entities.add(t.get('object', ''))
        
        entity_overlap = existing_entities & new_entities
        entity_coverage = len(entity_overlap) / len(new_entities) if new_entities else 0
        
        # 2. Relation coverage (predicate types)
        existing_relations = self._get_all_relations()
        new_relations = set(t.get('predicate', '') for t in new_triples)
        relation_overlap = existing_relations & new_relations
        relation_coverage = len(relation_overlap) / len(new_relations) if new_relations else 0
        
        # 3. Domain coverage (semantic categories)
        domains = self._analyze_domains(new_triples)
        
        # 4. Completeness score
        completeness = self._calculate_completeness(new_triples)
        
        # 5. Overall assessment
        overall_score = (entity_coverage * 0.4 + relation_coverage * 0.3 + completeness * 0.3)
        
        return {
            "entity_coverage": {
                "new_entities": len(new_entities),
                "existing_entities": len(existing_entities),
                "overlap": len(entity_overlap),
                "ratio": entity_coverage,
                "novel_entities": list(new_entities - existing_entities)[:10]
            },
            "relation_coverage": {
                "new_relations": list(new_relations),
                "existing_relations": list(existing_relations),
                "overlap": list(relation_overlap),
                "ratio": relation_coverage
            },
            "domains": domains,
            "completeness": completeness,
            "overall_score": overall_score,
            "assessment": self._get_assessment_label(overall_score),
            "recommendations": self._generate_recommendations(overall_score, new_triples)
        }
    
    def _get_all_entities(self) -> Set[str]:
        entities = set()
        for fact in self.reasoner.facts:
            entities.add(fact.subject)
            entities.add(fact.object)
        return entities
    
    def _get_all_relations(self) -> Set[str]:
        return set(f.predicate for f in self.reasoner.facts)
    
    def _analyze_domains(self, triples: List[Dict]) -> Dict:
        """Analyze domain distribution"""
        domains = {}
        for t in triples:
            subj = t.get('subject', '').lower()
            # Simple domain detection
            if any(w in subj for w in ['燃气', '调压', '压力', 'gas', 'regulator']):
                domains['gas_equipment'] = domains.get('gas_equipment', 0) + 1
            elif any(w in subj for w in ['供应商', '品牌', 'supplier', 'brand']):
                domains['supplier'] = domains.get('supplier', 0) + 1
            elif any(w in subj for w in ['标准', '规范', 'standard', 'spec']):
                domains['standard'] = domains.get('standard', 0) + 1
            else:
                domains['other'] = domains.get('other', 0) + 1
        return domains
    
    def _calculate_completeness(self, triples: List[Dict]) -> float:
        """Calculate structural completeness"""
        if not triples:
            return 0.0
        
        # Check for common relation types
        predicates = set(t.get('predicate', '') for t in triples)
        essential_relations = {'is_a', 'has', 'requires', '用途', '类型', '范围'}
        has_essential = len(predicates & essential_relations) / len(essential_relations)
        
        # Check for numeric values
        has_numeric = any(any(c.isdigit() for c in t.get('object', '')) for t in triples)
        
        return (has_essential * 0.7 + (0.3 if has_numeric else 0))
    
    def _get_assessment_label(self, score: float) -> str:
        if score < 0.3:
            return "🟢 High Novelty - Significant new knowledge"
        elif score < 0.6:
            return "🟡 Medium Overlap - Good extension"
        else:
            return "🔴 High Overlap - Mostly existing knowledge"
    
    def _generate_recommendations(self, score: float, triples: List[Dict]) -> List[str]:
        recs = []
        if score < 0.3:
            recs.append("✅ Good coverage of new domain")
        if not any(t.get('predicate', '').lower() in ['requires', '需要', 'requires'] for t in triples):
            recs.append("⚠️ Consider adding requirement relationships")
        if not any(any(c.isdigit() for c in t.get('object', '')) for t in triples):
            recs.append("⚠️ Consider adding numeric parameters")
        return recs if recs else ["✅ Knowledge structure looks good"]


# =========================================
# Graph Visualizer
# =========================================
class GraphVisualizer:
    """Generate interactive knowledge graph"""
    
    def __init__(self, reasoner: Reasoner):
        self.reasoner = reasoner
    
    def render(self, highlight_entities: List[str] = None) -> str:
        try:
            from pyvis.network import Network
            
            net = Network(height="500px", width="100%", bgcolor="#f8fafc", font_color="#1e293b", directed=True)
            net.toggle_physics(True)
            
            # Add all facts
            facts = list(self.reasoner.facts)
            highlight_set = set(highlight_entities or [])
            
            for fact in facts:
                # Determine node colors
                is_new = fact.subject in highlight_set or fact.object in highlight_set
                subj_color = "#ef4444" if is_new else "#6366f1"
                obj_color = "#f59e0b" if is_new else "#10b981"
                
                # Add nodes
                net.add_node(
                    fact.subject, 
                    label=fact.subject[:20],
                    color=subj_color,
                    size=25 if is_new else 20,
                    title=f"Entity: {fact.subject}"
                )
                net.add_node(
                    fact.object, 
                    label=fact.object[:20],
                    color=obj_color,
                    size=20,
                    title=f"Value: {fact.object}"
                )
                
                # Add edge
                net.add_edge(
                    fact.subject, 
                    fact.object,
                    label=fact.predicate[:15],
                    color="#6366f1" if is_new else "#94a3b8",
                    width=2 if is_new else 1,
                    title=f"{fact.predicate} (conf: {fact.confidence:.2f})"
                )
            
            # Save and return HTML
            path = "/tmp/clawra_graph.html"
            net.save_graph(path)
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"<div style='color:red'>Error rendering graph: {e}</div>"


# =========================================
# Enhanced Agent
# =========================================
class CompleteClawraAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.reasoner = Reasoner()
        self.rule_engine = RuleEngine()
        self.assessor = CoverageAssessor(self.reasoner)
        self.visualizer = GraphVisualizer(self.reasoner)
        self.execution_log = []
        self.last_extracted_entities = []
        
        self._init_base_knowledge()
    
    def _init_base_knowledge(self):
        base_facts = [
            Fact("燃气调压箱", "is_a", "燃气设备", 0.95),
            Fact("燃气调压箱", "用途", "降低燃气压力", 0.95),
            Fact("调压器", "类型", "直接作用式", 0.85),
            Fact("进口压力", "范围", "0.02-0.4 MPa", 0.95),
        ]
        for f in base_facts:
            self.reasoner.add_fact(f)
    
    def _log(self, msg: str):
        self.execution_log.append({"time": time.strftime("%H:%M:%S"), "message": msg})
    
    async def process(self, user_input: str) -> Dict:
        self.execution_log = []
        
        # Intent detection
        self._log("🔍 Analyzing intent...")
        
        if any(k in user_input.lower() for k in ['extract', '抽取', '提取']):
            return await self._handle_extraction(user_input)
        elif any(k in user_input.lower() for k in ['query', '查询', '什么是', '怎么', '如何']):
            return await self._handle_query(user_input)
        elif any(k in user_input.lower() for k in ['reason', '推理', '推导']):
            return await self._handle_reasoning()
        else:
            return await self._handle_chat(user_input)
    
    async def _handle_extraction(self, text: str) -> Dict:
        self._log("📝 Extracting knowledge with LLM...")
        
        clean_text = text.replace("Extract:", "").replace("extract:", "").strip()
        triples = await self.llm.extract_knowledge(clean_text)
        
        self._log(f"✅ Extracted {len(triples)} triples")
        
        # Add to KB
        added = []
        self.last_extracted_entities = []
        for t in triples:
            try:
                fact = Fact(t['subject'], t['predicate'], t['object'], 
                          t.get('confidence', 0.8), 'llm_extraction')
                self.reasoner.add_fact(fact)
                added.append(t)
                self.last_extracted_entities.extend([t['subject'], t['object']])
                self._log(f"💾 Added: {t['subject']} → {t['predicate']} → {t['object']}")
            except Exception as e:
                self._log(f"⚠️ Error: {e}")
        
        # Deep coverage assessment
        self._log("📊 Assessing coverage...")
        coverage = self.assessor.assess(triples)
        
        return {
            "type": "extraction",
            "triples": triples,
            "added_count": len(added),
            "total_facts": len(self.reasoner.facts),
            "coverage": coverage,
            "graph_html": self.visualizer.render(self.last_extracted_entities)
        }
    
    async def _handle_query(self, question: str) -> Dict:
        self._log("🔍 Searching knowledge base...")
        
        # Find relevant facts
        keywords = question.lower().split()
        relevant_facts = []
        for fact in self.reasoner.facts:
            fact_str = str(fact)
            score = sum(2 if kw in fact.subject.lower() else 1 if kw in fact_str.lower() else 0 
                       for kw in keywords)
            if score > 0:
                relevant_facts.append((score, fact_str))
        
        relevant_facts.sort(reverse=True)
        top_facts = [f[1] for f in relevant_facts[:10]]
        
        self._log(f"✅ Found {len(top_facts)} relevant facts")
        
        if not top_facts:
            return {
                "type": "query",
                "answer": "I don't have specific information about that. Try extracting some knowledge first.",
                "reasoning": [],
                "facts_used": 0
            }
        
        # Use LLM for reasoning
        self._log("🧠 Reasoning with LLM...")
        reasoning_result = await self.llm.answer_with_reasoning(question, top_facts)
        
        # Also try symbolic reasoning
        self._log("🔮 Attempting symbolic forward chaining...")
        inferred = self.reasoner.forward_chain(max_depth=2)
        self._log(f"✅ Inferred {len(inferred)} new facts")
        
        return {
            "type": "query",
            "answer": reasoning_result.get("answer", "No answer generated"),
            "reasoning": reasoning_result.get("reasoning_steps", []),
            "confidence": reasoning_result.get("confidence", 0.7),
            "facts_used": len(top_facts),
            "inferred_facts": [str(f) for f in inferred[:5]],
            "graph_html": self.visualizer.render()
        }
    
    async def _handle_reasoning(self) -> Dict:
        self._log("🧪 Running reasoning evaluation...")
        
        # Forward chaining
        inferred = self.reasoner.forward_chain(max_depth=3)
        
        return {
            "type": "reasoning",
            "inferred_count": len(inferred),
            "inferred_facts": [str(f) for f in inferred[:10]],
            "graph_html": self.visualizer.render()
        }
    
    async def _handle_chat(self, text: str) -> Dict:
        response = await self.llm.chat([
            {"role": "system", "content": f"You are Clawra. Knowledge base has {len(self.reasoner.facts)} facts."},
            {"role": "user", "content": text}
        ])
        
        return {
            "type": "chat",
            "response": response,
            "graph_html": self.visualizer.render()
        }


# =========================================
# Initialize
# =========================================
@st.cache_resource
def get_agent():
    return CompleteClawraAgent()

agent = get_agent()


# =========================================
# UI
# =========================================
st.title("🧠 Clawra Complete | Knowledge Graph & Deep Assessment")

st.markdown("""
**Complete features:**
1. 📊 **Interactive Knowledge Graph** - Visualize with PyVis
2. 📈 **Deep Coverage Assessment** - Entity/relation/completeness analysis
3. 🧠 **Enhanced Reasoning** - LLM + symbolic forward chaining
""")

# Sidebar
with st.sidebar:
    st.title("📊 Status")
    st.metric("Facts", len(agent.reasoner.facts))
    st.metric("Relations", len(set(f.predicate for f in agent.reasoner.facts)))
    
    st.markdown("---")
    st.markdown("**Quick Start:**")
    st.markdown("1. Type or paste knowledge text")
    st.markdown("2. Click Extract to visualize")
    st.markdown("3. Ask questions to test reasoning")

# Main area - tabs
tab1, tab2, tab3 = st.tabs(["💬 Chat & Extract", "🕸️ Knowledge Graph", "📈 Coverage Analysis"])

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None

with tab1:
    st.subheader("Knowledge Extraction & QA")
    
    # Display messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
            if "result" in msg and msg["result"].get("type") == "extraction":
                result = msg["result"]
                
                # Show triples
                st.markdown("**📚 Extracted Triples:**")
                for t in result.get("triples", [])[:20]:
                    st.markdown(f"<div class='triple-card'><b>{t['subject']}</b> → <code>{t['predicate']}</code> → <b>{t['object']}</b> <small>({t.get('confidence', 0.8):.0%})</small></div>", unsafe_allow_html=True)
                
                # Show coverage summary
                cov = result.get("coverage", {})
                score = cov.get("overall_score", 0)
                color_class = "coverage-high" if score < 0.3 else "coverage-medium" if score < 0.6 else "coverage-low"
                
                st.markdown(f"""
                **📊 Coverage Summary:**
                - Overall Score: <span class='{color_class}'>{score:.1%}</span>
                - Assessment: {cov.get('assessment', 'N/A')}
                - Entities: {cov.get('entity_coverage', {}).get('new_entities', 0)} new, {cov.get('entity_coverage', {}).get('overlap', 0)} overlap
                """, unsafe_allow_html=True)
            
            elif "result" in msg and msg["result"].get("type") == "query":
                result = msg["result"]
                
                # Show reasoning
                if result.get("reasoning"):
                    st.markdown("**🧠 Reasoning Steps:**")
                    for i, step in enumerate(result["reasoning"], 1):
                        st.markdown(f"{i}. {step}")
                
                st.markdown(f"**Confidence:** {result.get('confidence', 0.7):.0%}")
                st.markdown(f"**Facts Used:** {result.get('facts_used', 0)}")

# Input MUST be outside tabs
st.markdown("---")
if prompt := st.chat_input("Enter knowledge to extract or ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.spinner("🤖 Processing with LLM..."):
        result = asyncio.run(agent.process(prompt))
        st.session_state.last_result = result
        
        response_text = ""
        if result["type"] == "extraction":
            response_text = f"✅ Extracted {result['added_count']} triples. Total KB: {result['total_facts']} facts."
        elif result["type"] == "query":
            response_text = result.get("answer", "No answer generated.")
        elif result["type"] == "chat":
            response_text = result.get("response", "")
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": response_text,
            "result": result
        })
    
    st.experimental_rerun()

with tab2:
    st.subheader("Interactive Knowledge Graph")
    
    if st.session_state.last_result and "graph_html" in st.session_state.last_result:
        import streamlit.components.v1 as components
        components.html(st.session_state.last_result["graph_html"], height=520)
    else:
        # Show default graph
        import streamlit.components.v1 as components
        components.html(agent.visualizer.render(), height=520)
    
    st.info("💡 Graph shows all facts in knowledge base. Red/Yellow nodes = newly extracted entities.")

with tab3:
    st.subheader("Deep Coverage Assessment")
    
    if st.session_state.last_result and st.session_state.last_result.get("type") == "extraction":
        coverage = st.session_state.last_result.get("coverage", {})
        
        # Overall metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Overall Score", f"{coverage.get('overall_score', 0):.1%}")
        with col2:
            st.metric("Entity Coverage", f"{coverage.get('entity_coverage', {}).get('ratio', 0):.1%}")
        with col3:
            st.metric("Relation Coverage", f"{coverage.get('relation_coverage', {}).get('ratio', 0):.1%}")
        with col4:
            st.metric("Completeness", f"{coverage.get('completeness', 0):.1%}")
        
        # Assessment
        st.markdown(f"### {coverage.get('assessment', 'N/A')}")
        
        # Domain distribution
        st.markdown("**📊 Domain Distribution:**")
        domains = coverage.get("domains", {})
        for domain, count in domains.items():
            st.progress(count / max(domains.values()), text=f"{domain}: {count} facts")
        
        # Novel entities
        novel = coverage.get("entity_coverage", {}).get("novel_entities", [])
        if novel:
            st.markdown("**✨ Novel Entities (not in existing KB):**")
            st.write(", ".join(novel[:20]))
        
        # Recommendations
        st.markdown("**💡 Recommendations:**")
        for rec in coverage.get("recommendations", []):
            st.markdown(f"- {rec}")
    else:
        st.info("Extract knowledge first to see coverage analysis.")

st.markdown("---")

# Example inputs
st.subheader("📝 Example Inputs")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏥 Medical Example", use_container_width=True):
        example = """糖尿病患者需要定期监测血糖水平。正常空腹血糖应低于6.1 mmol/L。
        如果血糖超过11.1 mmol/L，需要注射胰岛素治疗。胰岛素治疗需要医生处方。"""
        st.session_state.messages.append({"role": "user", "content": example})
        st.experimental_rerun()

with col2:
    if st.button("⚖️ Legal Example", use_container_width=True):
        example = """合同违约是指一方未能履行合同义务。违约方需要承担赔偿责任。
        赔偿金额通常不超过合同总价的30%。违约金需要在判决后30天内支付。"""
        st.session_state.messages.append({"role": "user", "content": example})
        st.experimental_rerun()

with col3:
    if st.button("🔧 Engineering Example", use_container_width=True):
        example = """燃气调压箱是用于降低燃气压力的设备。进口压力范围为0.02-0.4 MPa。
        出口压力应稳定在2-5 kPa。调压箱需要每6个月进行一次维保检查。
        主要品牌包括特瑞斯、春晖、永良。供应商需要具备特种设备生产许可证。"""
        st.session_state.messages.append({"role": "user", "content": example})
        st.experimental_rerun()

st.markdown("---")
st.caption("🧠 Clawra Complete | VolcEngine Ark LLM | PyVis Graph | Deep Assessment")
