import json
from typing import List, Dict, Any
from .embedding_generator import EmbeddingGenerator

class KnowledgeBase:
    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()
        self.product_descriptions = self._load_product_descriptions()
        self.faq_content = self._load_faq_content()
        self.policy_content = self._load_policy_content()
    
    def _load_product_descriptions(self) -> List[Dict[str, Any]]:
        """Load enhanced product descriptions"""
        return [
            {
                "id": "product_001",
                "name": "My AI is Smarter Than Your Honor Student",
                "content": "My AI is Smarter Than Your Honor Student - A witty and humorous t-shirt perfect for tech enthusiasts, students, and AI researchers. This premium cotton t-shirt features a clever design that combines academic humor with artificial intelligence themes. Available in multiple sizes (S, M, L) and colors (Black, White, Light Blue). The design is printed using high-quality, fade-resistant ink that maintains its vibrant appearance wash after wash. Perfect for casual wear, campus life, or tech meetups.",
                "metadata": {
                    "type": "product",
                    "category": "humor",
                    "tags": ["ai", "humor", "student", "academic", "tech"],
                    "materials": ["100% cotton"],
                    "care": "Machine wash cold, tumble dry low",
                    "sizes": ["S", "M", "L"],
                    "colors": ["Black", "White", "Light Blue"]
                }
            },
            {
                "id": "product_002", 
                "name": "Keep Calm and Trust the Neural Network",
                "content": "Keep Calm and Trust the Neural Network - A stylish t-shirt featuring a modern take on the classic 'Keep Calm' design with a machine learning twist. This comfortable t-shirt is made from soft, breathable cotton and features a neural network-inspired graphic. Perfect for data scientists, machine learning engineers, and anyone who appreciates the power of neural networks. The design is subtle yet distinctive, making it suitable for both casual and semi-professional settings.",
                "metadata": {
                    "type": "product",
                    "category": "inspirational",
                    "tags": ["neural network", "machine learning", "data science", "calm"],
                    "materials": ["100% cotton"],
                    "care": "Machine wash cold, tumble dry low",
                    "sizes": ["S", "M", "L"],
                    "colors": ["Black", "Pink"]
                }
            },
            {
                "id": "product_003",
                "name": "I'm Just Here for the Deep Learning",
                "content": "I'm Just Here for the Deep Learning - A clever t-shirt for deep learning enthusiasts and researchers. This design combines humor with technical expertise, perfect for those who spend their days training neural networks and analyzing complex datasets. The t-shirt features a minimalist design that speaks to the focused nature of deep learning work. Made from premium cotton for maximum comfort during long coding sessions or research work.",
                "metadata": {
                    "type": "product", 
                    "category": "humor",
                    "tags": ["deep learning", "neural networks", "research", "coding"],
                    "materials": ["100% cotton"],
                    "care": "Machine wash cold, tumble dry low",
                    "sizes": ["S", "M"],
                    "colors": ["White"]
                }
            }
        ]
    
    def _load_faq_content(self) -> List[Dict[str, Any]]:
        """Load FAQ content"""
        return [
            {
                "id": "faq_001",
                "question": "What are your shipping options and delivery times?",
                "content": "We offer standard shipping (3-5 business days) and express shipping (1-2 business days). Standard shipping costs $5.99, while express shipping costs $12.99. All orders are processed within 24 hours of placement. You'll receive a tracking number via email once your order ships.",
                "metadata": {
                    "type": "faq",
                    "category": "shipping",
                    "tags": ["shipping", "delivery", "tracking"]
                }
            },
            {
                "id": "faq_002",
                "question": "What is your return and exchange policy?",
                "content": "We offer a 30-day return policy for all unworn, unwashed items with original tags attached. Returns are free for defective items. For size exchanges, we'll cover the return shipping cost. To initiate a return, please contact our customer service team with your order number.",
                "metadata": {
                    "type": "faq",
                    "category": "returns",
                    "tags": ["returns", "exchanges", "refunds", "policy"]
                }
            },
            {
                "id": "faq_003",
                "question": "How do I determine the right size for me?",
                "content": "Our t-shirts follow standard US sizing. For the best fit, measure your chest circumference and refer to our size chart: Small (34-36 inches), Medium (38-40 inches), Large (42-44 inches). If you're between sizes, we recommend sizing up for a more comfortable fit.",
                "metadata": {
                    "type": "faq",
                    "category": "sizing",
                    "tags": ["sizing", "fit", "measurements", "size chart"]
                }
            },
            {
                "id": "faq_004",
                "question": "What payment methods do you accept?",
                "content": "We accept all major credit cards (Visa, MasterCard, American Express, Discover), PayPal, and Apple Pay. All payments are processed securely through our encrypted payment system. We never store your payment information on our servers.",
                "metadata": {
                    "type": "faq",
                    "category": "payment",
                    "tags": ["payment", "credit cards", "paypal", "security"]
                }
            },
            {
                "id": "faq_005",
                "question": "How do I care for my t-shirt?",
                "content": "To maintain the quality and longevity of your t-shirt, machine wash cold with like colors, tumble dry low, and avoid using bleach or fabric softeners. Iron on low heat if needed. The high-quality printing will maintain its vibrant appearance for years with proper care.",
                "metadata": {
                    "type": "faq",
                    "category": "care",
                    "tags": ["care", "washing", "maintenance", "longevity"]
                }
            }
        ]
    
    def _load_policy_content(self) -> List[Dict[str, Any]]:
        """Load policy content"""
        return [
            {
                "id": "policy_001",
                "title": "Shipping Policy",
                "content": "We ship to all 50 US states and most international locations. Standard shipping takes 3-5 business days and costs $5.99. Express shipping takes 1-2 business days and costs $12.99. International shipping costs vary by location. All orders are processed within 24 hours and include tracking information.",
                "metadata": {
                    "type": "policy",
                    "category": "shipping",
                    "tags": ["shipping", "delivery", "international", "tracking"]
                }
            },
            {
                "id": "policy_002",
                "title": "Return and Refund Policy", 
                "content": "We offer a 30-day return window for all unworn, unwashed items with original tags. Returns are free for defective items. For size exchanges, we cover return shipping. Refunds are processed within 5-7 business days of receiving returned items. Sale items are final sale unless defective.",
                "metadata": {
                    "type": "policy",
                    "category": "returns",
                    "tags": ["returns", "refunds", "exchanges", "defective"]
                }
            },
            {
                "id": "policy_003",
                "title": "Privacy Policy",
                "content": "We collect only necessary information to process your orders and provide customer service. We never sell or share your personal information with third parties. Payment information is encrypted and processed securely. You can request deletion of your data at any time.",
                "metadata": {
                    "type": "policy",
                    "category": "privacy",
                    "tags": ["privacy", "data", "security", "personal information"]
                }
            }
        ]
    
    def get_all_content(self) -> Dict[str, List[Dict]]:
        """Get all knowledge base content"""
        return {
            "products": self.product_descriptions,
            "faq": self.faq_content,
            "policies": self.policy_content
        }
    
    def create_product_vectors(self) -> List[Dict]:
        """Create vector entries for product descriptions"""
        vectors = []
        for product in self.product_descriptions:
            vector_entry = self.embedding_generator.create_vector_entry(
                product["content"],
                product["metadata"]
            )
            vector_entry["id"] = product["id"]
            vectors.append(vector_entry)
        return vectors
    
    def create_faq_vectors(self) -> List[Dict]:
        """Create vector entries for FAQ content"""
        vectors = []
        for faq in self.faq_content:
            content = f"Question: {faq['question']} Answer: {faq['content']}"
            vector_entry = self.embedding_generator.create_vector_entry(
                content,
                faq["metadata"]
            )
            vector_entry["id"] = faq["id"]
            vectors.append(vector_entry)
        return vectors
    
    def create_policy_vectors(self) -> List[Dict]:
        """Create vector entries for policy content"""
        vectors = []
        for policy in self.policy_content:
            vector_entry = self.embedding_generator.create_vector_entry(
                policy["content"],
                policy["metadata"]
            )
            vector_entry["id"] = policy["id"]
            vectors.append(vector_entry)
        return vectors 