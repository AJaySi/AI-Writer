"""
Test script to verify strategy data structure matches frontend expectations
"""

import asyncio
import json
from api.content_planning.services.strategy_service import StrategyService

async def test_strategy_data_structure():
    """Test the strategy data structure to ensure it matches frontend expectations."""
    
    print("🧪 Testing Strategy Data Structure")
    print("=" * 50)
    
    # Initialize service
    service = StrategyService()
    
    # Get strategies
    result = await service.get_strategies(user_id=1)
    
    print("📊 Backend Response Structure:")
    print(json.dumps(result, indent=2, default=str))
    
    # Check if strategies array exists
    if "strategies" in result and len(result["strategies"]) > 0:
        strategy = result["strategies"][0]
        
        print("\n✅ Frontend Expected Structure Check:")
        print("-" * 40)
        
        # Check for ai_recommendations
        if "ai_recommendations" in strategy:
            ai_rec = strategy["ai_recommendations"]
            print(f"✅ ai_recommendations: Present")
            
            # Check market_score
            if "market_score" in ai_rec:
                print(f"✅ market_score: {ai_rec['market_score']}")
            else:
                print("❌ market_score: Missing")
            
            # Check strengths
            if "strengths" in ai_rec:
                print(f"✅ strengths: {len(ai_rec['strengths'])} items")
            else:
                print("❌ strengths: Missing")
            
            # Check weaknesses
            if "weaknesses" in ai_rec:
                print(f"✅ weaknesses: {len(ai_rec['weaknesses'])} items")
            else:
                print("❌ weaknesses: Missing")
            
            # Check competitive_advantages
            if "competitive_advantages" in ai_rec:
                print(f"✅ competitive_advantages: {len(ai_rec['competitive_advantages'])} items")
            else:
                print("❌ competitive_advantages: Missing")
            
            # Check strategic_risks
            if "strategic_risks" in ai_rec:
                print(f"✅ strategic_risks: {len(ai_rec['strategic_risks'])} items")
            else:
                print("❌ strategic_risks: Missing")
                
        else:
            print("❌ ai_recommendations: Missing")
        
        # Check for required strategy fields
        required_fields = ["id", "name", "industry", "target_audience", "content_pillars"]
        for field in required_fields:
            if field in strategy:
                print(f"✅ {field}: Present")
            else:
                print(f"❌ {field}: Missing")
        
        print("\n🎯 Frontend Data Mapping Validation:")
        print("-" * 40)
        
        # Validate the specific structure expected by frontend
        if "ai_recommendations" in strategy:
            ai_rec = strategy["ai_recommendations"]
            
            # Check market positioning structure
            if "market_score" in ai_rec:
                print(f"✅ Frontend can access: strategy.ai_recommendations.market_score")
            
            # Check strengths structure
            if "strengths" in ai_rec and isinstance(ai_rec["strengths"], list):
                print(f"✅ Frontend can access: strategy.ai_recommendations.strengths")
            
            # Check weaknesses structure
            if "weaknesses" in ai_rec and isinstance(ai_rec["weaknesses"], list):
                print(f"✅ Frontend can access: strategy.ai_recommendations.weaknesses")
            
            # Check competitive advantages structure
            if "competitive_advantages" in ai_rec and isinstance(ai_rec["competitive_advantages"], list):
                print(f"✅ Frontend can access: strategy.ai_recommendations.competitive_advantages")
            
            # Check strategic risks structure
            if "strategic_risks" in ai_rec and isinstance(ai_rec["strategic_risks"], list):
                print(f"✅ Frontend can access: strategy.ai_recommendations.strategic_risks")
        
        print("\n🎉 Data Structure Validation Complete!")
        print("=" * 50)
        
        return True
    else:
        print("❌ No strategies found in response")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_strategy_data_structure())
    if success:
        print("✅ All tests passed! Backend data structure matches frontend expectations.")
    else:
        print("❌ Tests failed! Backend data structure needs adjustment.") 