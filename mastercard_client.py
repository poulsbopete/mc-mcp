"""Mastercard API client with mock and real implementations."""
import time
import random
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
from opentelemetry import trace

from config import settings

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


class MastercardClient:
    """
    Client for Mastercard APIs with automatic tracing.
    Supports both mock mode (for demo) and real API calls.
    """
    
    def __init__(self, mock_mode: bool = True):
        self.mock_mode = mock_mode or settings.enable_mock_mode
        self.base_url = "https://api.mastercard.com"
        
        if not self.mock_mode:
            # Initialize real Mastercard SDK
            self._init_real_client()
        
        logger.info(f"MastercardClient initialized (mock_mode={self.mock_mode})")
    
    def _init_real_client(self):
        """Initialize real Mastercard API client with OAuth."""
        # This would use the actual Mastercard SDK
        # For demo purposes, we'll use mock mode
        pass
    
    @tracer.start_as_current_span("mastercard.open_banking.get_accounts")
    def get_banking_accounts(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieve banking accounts using Mastercard Open Banking API.
        
        Args:
            user_id: The user identifier
            
        Returns:
            Dictionary containing account information
        """
        span = trace.get_current_span()
        span.set_attribute("user.id", user_id)
        span.set_attribute("api.name", "open_banking")
        span.set_attribute("api.operation", "get_accounts")
        
        logger.info(f"Fetching accounts for user {user_id}")
        
        if self.mock_mode:
            # Simulate API latency
            time.sleep(random.uniform(0.1, 0.3))
            
            accounts = [
                {
                    "account_id": f"acc_{random.randint(1000, 9999)}",
                    "account_type": "checking",
                    "balance": round(random.uniform(1000, 50000), 2),
                    "currency": "USD",
                    "status": "active"
                },
                {
                    "account_id": f"acc_{random.randint(1000, 9999)}",
                    "account_type": "savings",
                    "balance": round(random.uniform(5000, 100000), 2),
                    "currency": "USD",
                    "status": "active"
                }
            ]
            
            span.set_attribute("account.count", len(accounts))
            logger.info(f"Retrieved {len(accounts)} accounts for user {user_id}")
            
            return {
                "user_id": user_id,
                "accounts": accounts,
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            # Real API call would go here
            raise NotImplementedError("Real Mastercard API not configured")
    
    @tracer.start_as_current_span("mastercard.merchant.locate")
    def locate_merchants(self, query: str, latitude: float = 37.7749, longitude: float = -122.4194, radius: int = 5) -> Dict[str, Any]:
        """
        Locate merchants using Mastercard Merchant Identifier API.
        
        Args:
            query: Search query (e.g., "coffee", "restaurant")
            latitude: Location latitude
            longitude: Location longitude
            radius: Search radius in miles
            
        Returns:
            Dictionary containing merchant results
        """
        span = trace.get_current_span()
        span.set_attribute("merchant.query", query)
        span.set_attribute("location.latitude", latitude)
        span.set_attribute("location.longitude", longitude)
        span.set_attribute("search.radius", radius)
        
        logger.info(f"Searching merchants: query={query}, location=({latitude}, {longitude})")
        
        if self.mock_mode:
            time.sleep(random.uniform(0.15, 0.4))
            
            merchants = [
                {
                    "merchant_id": f"mch_{random.randint(10000, 99999)}",
                    "name": f"{query.title()} Shop {i+1}",
                    "category": query,
                    "address": f"{random.randint(100, 9999)} Market St, San Francisco, CA",
                    "distance": round(random.uniform(0.1, radius), 2),
                    "rating": round(random.uniform(3.5, 5.0), 1),
                    "accepts_mastercard": True
                }
                for i in range(random.randint(5, 15))
            ]
            
            span.set_attribute("merchant.count", len(merchants))
            logger.info(f"Found {len(merchants)} merchants for query: {query}")
            
            return {
                "query": query,
                "location": {"latitude": latitude, "longitude": longitude},
                "radius_miles": radius,
                "merchants": merchants,
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            raise NotImplementedError("Real Mastercard API not configured")
    
    @tracer.start_as_current_span("mastercard.fraud.check_transaction")
    def check_fraud(self, transaction_id: str, amount: float, merchant_id: str = None) -> Dict[str, Any]:
        """
        Check transaction for fraud using Mastercard Decision Intelligence.
        
        Args:
            transaction_id: Unique transaction identifier
            amount: Transaction amount
            merchant_id: Optional merchant identifier
            
        Returns:
            Dictionary containing fraud analysis results
        """
        span = trace.get_current_span()
        span.set_attribute("transaction.id", transaction_id)
        span.set_attribute("transaction.amount", amount)
        if merchant_id:
            span.set_attribute("merchant.id", merchant_id)
        
        logger.info(f"Checking fraud for transaction {transaction_id}, amount: ${amount}")
        
        if self.mock_mode:
            time.sleep(random.uniform(0.2, 0.5))
            
            # Simulate fraud detection logic
            risk_score = random.uniform(0, 100)
            is_suspicious = risk_score > 70 or amount > 5000
            
            risk_factors = []
            if amount > 5000:
                risk_factors.append("high_amount")
            if risk_score > 80:
                risk_factors.append("unusual_pattern")
            if random.random() > 0.8:
                risk_factors.append("new_merchant")
            
            result = {
                "transaction_id": transaction_id,
                "amount": amount,
                "risk_score": round(risk_score, 2),
                "status": "flagged" if is_suspicious else "approved",
                "risk_factors": risk_factors,
                "recommendation": "review" if is_suspicious else "approve",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            span.set_attribute("fraud.risk_score", result["risk_score"])
            span.set_attribute("fraud.status", result["status"])
            
            logger.warning(f"Transaction {transaction_id}: {result['status']} (risk: {result['risk_score']})")
            
            return result
        else:
            raise NotImplementedError("Real Mastercard API not configured")
    
    @tracer.start_as_current_span("mastercard.transactions.history")
    def get_transaction_history(self, account_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Get transaction history for an account.
        
        Args:
            account_id: Account identifier
            days: Number of days to look back
            
        Returns:
            Dictionary containing transaction history
        """
        span = trace.get_current_span()
        span.set_attribute("account.id", account_id)
        span.set_attribute("history.days", days)
        
        logger.info(f"Fetching {days} days of transactions for account {account_id}")
        
        if self.mock_mode:
            time.sleep(random.uniform(0.2, 0.5))
            
            num_transactions = random.randint(10, 50)
            transactions = []
            
            categories = ["grocery", "restaurant", "gas", "shopping", "entertainment", "utilities"]
            
            for i in range(num_transactions):
                date = datetime.utcnow() - timedelta(days=random.randint(0, days))
                transactions.append({
                    "transaction_id": f"txn_{random.randint(100000, 999999)}",
                    "date": date.isoformat(),
                    "merchant": f"Merchant {random.randint(1, 100)}",
                    "category": random.choice(categories),
                    "amount": round(random.uniform(5, 500), 2),
                    "currency": "USD",
                    "status": "completed"
                })
            
            # Sort by date descending
            transactions.sort(key=lambda x: x["date"], reverse=True)
            
            span.set_attribute("transaction.count", len(transactions))
            logger.info(f"Retrieved {len(transactions)} transactions for account {account_id}")
            
            return {
                "account_id": account_id,
                "period_days": days,
                "transactions": transactions,
                "total_spent": round(sum(t["amount"] for t in transactions), 2),
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            raise NotImplementedError("Real Mastercard API not configured")

