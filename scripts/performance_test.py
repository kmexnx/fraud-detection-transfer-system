#!/usr/bin/env python3
"""
Basic performance testing script.

This script runs basic performance tests against the fraud detection API.
For more comprehensive testing, consider using tools like Locust or Artillery.
"""

import asyncio
import time
import statistics
from typing import List
import httpx
import json


class PerformanceTest:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = []
    
    async def get_auth_token(self) -> str:
        """Get authentication token for testing."""
        async with httpx.AsyncClient() as client:
            # Login with test user (assuming seeded database)
            response = await client.post(
                f"{self.base_url}/api/v1/auth/token",
                data={"username": "alice", "password": "password123"},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            if response.status_code == 200:
                return response.json()["access_token"]
            else:
                raise Exception(f"Failed to get auth token: {response.status_code}")
    
    async def measure_request(self, method: str, url: str, **kwargs) -> dict:
        """Measure a single HTTP request."""
        start_time = time.time()
        
        async with httpx.AsyncClient() as client:
            try:
                if method.upper() == "GET":
                    response = await client.get(url, **kwargs)
                elif method.upper() == "POST":
                    response = await client.post(url, **kwargs)
                elif method.upper() == "PATCH":
                    response = await client.patch(url, **kwargs)
                else:
                    raise ValueError(f"Unsupported method: {method}")
                
                end_time = time.time()
                duration = (end_time - start_time) * 1000  # Convert to milliseconds
                
                return {
                    "duration_ms": duration,
                    "status_code": response.status_code,
                    "success": 200 <= response.status_code < 400,
                    "response_size": len(response.content)
                }
            except Exception as e:
                end_time = time.time()
                duration = (end_time - start_time) * 1000
                return {
                    "duration_ms": duration,
                    "status_code": 0,
                    "success": False,
                    "error": str(e),
                    "response_size": 0
                }
    
    async def test_endpoint_performance(self, 
                                      name: str,
                                      method: str,
                                      endpoint: str,
                                      num_requests: int = 100,
                                      concurrent: int = 10,
                                      **kwargs) -> dict:
        """Test performance of a specific endpoint."""
        print(f"\nTesting {name}...")
        print(f"Requests: {num_requests}, Concurrent: {concurrent}")
        
        url = f"{self.base_url}{endpoint}"
        
        # Create semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(concurrent)
        
        async def make_request():
            async with semaphore:
                return await self.measure_request(method, url, **kwargs)
        
        # Run all requests
        start_time = time.time()
        tasks = [make_request() for _ in range(num_requests)]
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time
        
        # Analyze results
        durations = [r["duration_ms"] for r in results if r["success"]]
        successes = sum(1 for r in results if r["success"])
        failures = len(results) - successes
        
        if durations:
            stats = {
                "test_name": name,
                "endpoint": endpoint,
                "total_requests": num_requests,
                "successful_requests": successes,
                "failed_requests": failures,
                "success_rate": successes / num_requests * 100,
                "total_time_seconds": total_time,
                "requests_per_second": num_requests / total_time,
                "avg_response_time_ms": statistics.mean(durations),
                "min_response_time_ms": min(durations),
                "max_response_time_ms": max(durations),
                "median_response_time_ms": statistics.median(durations),
                "p95_response_time_ms": self.percentile(durations, 95),
                "p99_response_time_ms": self.percentile(durations, 99)
            }
        else:
            stats = {
                "test_name": name,
                "endpoint": endpoint,
                "total_requests": num_requests,
                "successful_requests": 0,
                "failed_requests": num_requests,
                "success_rate": 0,
                "error": "All requests failed"
            }
        
        self.results.append(stats)
        self.print_test_results(stats)
        return stats
    
    def percentile(self, data: List[float], percentile: float) -> float:
        """Calculate percentile of a list."""
        if not data:
            return 0
        
        sorted_data = sorted(data)
        k = (len(sorted_data) - 1) * (percentile / 100)
        f = int(k)
        c = k - f
        
        if f == len(sorted_data) - 1:
            return sorted_data[f]
        else:
            return sorted_data[f] * (1 - c) + sorted_data[f + 1] * c
    
    def print_test_results(self, stats: dict):
        """Print formatted test results."""
        print(f"  ✓ Success Rate: {stats.get('success_rate', 0):.1f}%")
        if 'avg_response_time_ms' in stats:
            print(f"  ✓ Avg Response Time: {stats['avg_response_time_ms']:.2f}ms")
            print(f"  ✓ P95 Response Time: {stats['p95_response_time_ms']:.2f}ms")
            print(f"  ✓ P99 Response Time: {stats['p99_response_time_ms']:.2f}ms")
            print(f"  ✓ Requests/Second: {stats['requests_per_second']:.2f}")
    
    def print_summary(self):
        """Print overall test summary."""
        print("\n" + "="*60)
        print("PERFORMANCE TEST SUMMARY")
        print("="*60)
        
        for result in self.results:
            if 'error' in result:
                print(f"\n❌ {result['test_name']}: FAILED")
                print(f"   Error: {result['error']}")
            else:
                print(f"\n✅ {result['test_name']}")
                print(f"   Success Rate: {result['success_rate']:.1f}%")
                print(f"   Avg Response: {result.get('avg_response_time_ms', 0):.2f}ms")
                print(f"   RPS: {result.get('requests_per_second', 0):.2f}")
        
        # Overall statistics
        successful_tests = [r for r in self.results if 'error' not in r]
        if successful_tests:
            avg_success_rate = statistics.mean([r['success_rate'] for r in successful_tests])
            avg_response_time = statistics.mean([r.get('avg_response_time_ms', 0) for r in successful_tests])
            total_rps = sum([r.get('requests_per_second', 0) for r in successful_tests])
            
            print(f"\n📊 OVERALL METRICS")
            print(f"   Tests Passed: {len(successful_tests)}/{len(self.results)}")
            print(f"   Avg Success Rate: {avg_success_rate:.1f}%")
            print(f"   Avg Response Time: {avg_response_time:.2f}ms")
            print(f"   Combined RPS: {total_rps:.2f}")


async def main():
    """Run performance tests."""
    tester = PerformanceTest()
    
    print("🚀 Starting Performance Tests...")
    print("Make sure the application is running and database is seeded!")
    
    try:
        # Get auth token
        print("\n🔐 Getting authentication token...")
        token = await tester.get_auth_token()
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test health endpoint (no auth required)
        await tester.test_endpoint_performance(
            name="Health Check",
            method="GET",
            endpoint="/health",
            num_requests=50,
            concurrent=10
        )
        
        # Test authentication endpoint
        await tester.test_endpoint_performance(
            name="User Profile",
            method="GET",
            endpoint="/api/v1/auth/me",
            num_requests=100,
            concurrent=20,
            headers=auth_headers
        )
        
        # Test transfers list endpoint
        await tester.test_endpoint_performance(
            name="Transfers List",
            method="GET",
            endpoint="/api/v1/transfers",
            num_requests=100,
            concurrent=15,
            headers=auth_headers
        )
        
        # Test transfer statistics
        await tester.test_endpoint_performance(
            name="Transfer Statistics",
            method="GET",
            endpoint="/api/v1/transfers/stats/summary",
            num_requests=50,
            concurrent=10,
            headers=auth_headers
        )
        
        # Test fraud risk score
        await tester.test_endpoint_performance(
            name="Fraud Risk Score",
            method="GET",
            endpoint="/api/v1/fraud/risk-score",
            num_requests=75,
            concurrent=15,
            headers=auth_headers
        )
        
        # Test transfer creation (more intensive)
        transfer_data = {
            "amount": 100.0,
            "currency": "USD",
            "description": "Performance test transfer",
            "receiver_id": 2,  # Assuming Bob exists from seeded data
            "transfer_type": "internal"
        }
        
        await tester.test_endpoint_performance(
            name="Create Transfer",
            method="POST",
            endpoint="/api/v1/transfers",
            num_requests=30,  # Fewer requests since this creates data
            concurrent=5,
            headers=auth_headers,
            json=transfer_data
        )
        
    except Exception as e:
        print(f"\n❌ Error during performance testing: {e}")
        print("Make sure the application is running and accessible.")
    
    finally:
        # Print summary
        tester.print_summary()


if __name__ == "__main__":
    asyncio.run(main())