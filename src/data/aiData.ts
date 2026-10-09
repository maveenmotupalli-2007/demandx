export interface AIPromptResponse {
  question: string;
  answer: string;
  category: string;
}

export const AI_SUGGESTIONS = [
  "Why is tomato demand increasing?",
  "What should I stock next week?",
  "Best time to buy?",
  "Show market opportunities",
  "Compare products"
];

export const AI_KNOWLEDGE_BASE: Record<string, string> = {
  "why is tomato demand increasing?": 
    "Tomato demand is currently surging by +24% across AP & South India due to seasonal consumption spikes, low harvest yields in neighboring districts, and increased procurement by regional food processors in Guntur & Vijayawada.",
    
  "what should i stock next week?": 
    "Based on real-time market trends, we recommend stocking up on Tomato (+24% demand surge) and Red Chilli (+28% projected spike). Keep Potato inventory moderate as market supply is currently surplus.",
    
  "best time to buy?": 
    "For Tomatoes: Market prices are expected to drop by ~15% late next week as fresh harvests enter Vijayawada markets. For Red Chilli: Current prices are stable, but projected to rise by 20% next month. Buy chilli stock now!",
    
  "show market opportunities": 
    "Key Opportunities Identified:\n1. South India Chilli Supply Shortage (+26% price premium opportunity)\n2. High Retail Velocity for Packaged Sauce in Urban AP\n3. Export Demand Spike for Guntur Spices",
    
  "compare products": 
    "Comparing Tomato vs Red Chilli:\n• Tomato: High volume, 24% growth, short shelf-life (requires fast retail turnaround).\n• Red Chilli: High margin, 28% growth, long shelf-life (optimal for inventory buildup and supplier contracts).",

  "default":
    "Based on DemandX market intelligence for India: Market activity shows steady +18% growth across agricultural commodities. Inventory optimization can reduce spoilage waste by up to 30% while increasing overall gross margins by 18-22%."
};
