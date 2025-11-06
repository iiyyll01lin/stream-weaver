#!/usr/bin/env python3
"""
Phase 1 Integration Test Script (Python Version)
Integration Test Script for Phase 1

Purpose: Verify API service and algorithm integration works correctly
Usage: python3 test_phase1_integration.py
"""

import sys
import time
import requests
from typing import Dict, Any, List, Tuple

# Configuration
API_BASE_URL = "http://localhost:8000"
TIMEOUT = 10  # seconds


class Colors:
    """Terminal color codes"""
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


class TestRunner:
    """Test runner"""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_results: List[Tuple[str, bool, str]] = []
    
    def run_test(self, name: str, test_func, *args, **kwargs) -> bool:
        """Execute a single test"""
        print(f"Test: {name} ... ", end='', flush=True)
        
        try:
            test_func(*args, **kwargs)
            print(f"{Colors.GREEN}✓ Passed{Colors.NC}")
            self.tests_passed += 1
            self.test_results.append((name, True, ""))
            return True
        except AssertionError as e:
            print(f"{Colors.RED}✗ Failed{Colors.NC}")
            self.tests_failed += 1
            self.test_results.append((name, False, str(e)))
            return False
        except Exception as e:
            print(f"{Colors.RED}✗ Error{Colors.NC} ({str(e)})")
            self.tests_failed += 1
            self.test_results.append((name, False, str(e)))
            return False
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 50)
        print("Test Summary")
        print("=" * 50)
        print(f"{Colors.GREEN}Passed: {self.tests_passed}{Colors.NC}")
        print(f"{Colors.RED}Failed: {self.tests_failed}{Colors.NC}")
        
        if self.tests_failed > 0:
            print(f"\n{Colors.RED}Failed tests:{Colors.NC}")
            for name, passed, error in self.test_results:
                if not passed:
                    print(f"  - {name}")
                    if error:
                        print(f"    Error: {error}")
        
        print("\n" + "=" * 50)
        
        if self.tests_failed == 0:
            print(f"{Colors.GREEN}🎉 All tests passed!{Colors.NC}\n")
            return 0
        else:
            print(f"{Colors.RED}❌ Some tests failed{Colors.NC}\n")
            return 1


# Test function definitions

def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f"{API_BASE_URL}/health", timeout=TIMEOUT)
    assert response.status_code == 200, f"Status code should be 200, got {response.status_code}"
    data = response.json()
    assert data["status"] == "healthy", "Status should be healthy"
    assert data["algo_available"] is True, "Algorithm should be available"


def test_optimize_min_stations():
    """Test min_stations optimization"""
    response = requests.post(
        f"{API_BASE_URL}/optimize",
        json={
            "work_order_id": "WO_A",
            "target_takt": 80000,
            "optimization_goal": "min_stations"
        },
        timeout=TIMEOUT
    )
    assert response.status_code == 200, f"Status code should be 200, got {response.status_code}"
    data = response.json()
    
    # Verify required fields
    assert "work_order_id" in data, "Response should contain work_order_id"
    assert "line_count" in data, "Response should contain line_count"
    assert "stations" in data, "Response should contain stations"
    assert "takt_time_ms" in data, "Response should contain takt_time_ms"
    
    # Verify value ranges
    assert data["line_count"] > 0, "Number of stations should be > 0"
    assert 0 <= data["utilization_avg"] <= 100, "Utilization should be between 0~100"


def test_optimize_work_order(work_order_id: str):
    """Test optimization for specific work order"""
    response = requests.post(
        f"{API_BASE_URL}/optimize",
        json={
            "work_order_id": work_order_id,
            "target_takt": 80000,
            "optimization_goal": "min_stations"
        },
        timeout=TIMEOUT
    )
    assert response.status_code == 200, f"Work order {work_order_id} should optimize successfully"
    data = response.json()
    assert data["work_order_id"] == work_order_id, "Response work order ID should match"


def test_optimize_goal(goal: str):
    """Test specific optimization objective"""
    response = requests.post(
        f"{API_BASE_URL}/optimize",
        json={
            "work_order_id": "WO_A",
            "target_takt": 80000,
            "optimization_goal": goal
        },
        timeout=TIMEOUT
    )
    assert response.status_code == 200, f"Objective {goal} should execute successfully"
    data = response.json()
    assert data["objectives"]["goal"] == goal, "Response objective should match"


def test_workstations_endpoint():
    """Test workstations endpoint"""
    response = requests.get(
        f"{API_BASE_URL}/workstations",
        params={
            "work_order_id": "WO_A",
            "target_takt": 80000
        },
        timeout=TIMEOUT
    )
    assert response.status_code == 200, "Workstations query should succeed"
    data = response.json()
    assert isinstance(data, list), "Response should be a list"
    assert len(data) > 0, "Should have at least one workstation"


def test_takt_summary_endpoint():
    """Test takt summary endpoint"""
    response = requests.get(
        f"{API_BASE_URL}/takt-summary",
        params={
            "work_order_id": "WO_A",
            "target_takt": 80000
        },
        timeout=TIMEOUT
    )
    assert response.status_code == 200, "Takt summary query should succeed"
    data = response.json()
    assert "achieved_takt" in data, "Response should contain achieved_takt"
    assert "efficiency_pct" in data, "Response should contain efficiency_pct"


def test_dashboard_endpoint():
    """Test Dashboard endpoint"""
    response = requests.get(f"{API_BASE_URL}/", timeout=TIMEOUT)
    assert response.status_code == 200, "Dashboard should be accessible"
    assert "text/html" in response.headers.get("Content-Type", ""), "Should return HTML"


def test_swagger_docs():
    """Test Swagger documentation endpoint"""
    response = requests.get(f"{API_BASE_URL}/api/docs", timeout=TIMEOUT)
    assert response.status_code == 200, "API documentation should be accessible"


def test_invalid_work_order():
    """Test invalid work order ID (should return error)"""
    response = requests.post(
        f"{API_BASE_URL}/optimize",
        json={
            "work_order_id": "INVALID_WO",
            "target_takt": 80000,
            "optimization_goal": "min_stations"
        },
        timeout=TIMEOUT
    )
    assert response.status_code == 400, "Invalid work order should return 400"
    data = response.json()
    assert "detail" in data, "Error response should contain detail"


def test_invalid_goal():
    """Test invalid optimization objective (should return error)"""
    response = requests.post(
        f"{API_BASE_URL}/optimize",
        json={
            "work_order_id": "WO_A",
            "target_takt": 80000,
            "optimization_goal": "invalid_goal"
        },
        timeout=TIMEOUT
    )
    assert response.status_code == 400, "Invalid objective should return 400"


def test_negative_takt():
    """Test negative takt time (should return error)"""
    response = requests.post(
        f"{API_BASE_URL}/optimize",
        json={
            "work_order_id": "WO_A",
            "target_takt": -1000,
            "optimization_goal": "min_stations"
        },
        timeout=TIMEOUT
    )
    assert response.status_code == 422, "Negative takt should return 422"


def test_performance():
    """Test API performance (average of 3 runs should be < 3 seconds)"""
    times = []
    for _ in range(3):
        start = time.time()
        response = requests.post(
            f"{API_BASE_URL}/optimize",
            json={
                "work_order_id": "WO_A",
                "target_takt": 80000,
                "optimization_goal": "min_stations"
            },
            timeout=TIMEOUT
        )
        elapsed = time.time() - start
        times.append(elapsed)
        assert response.status_code == 200, "Performance test request should succeed"
    
    avg_time = sum(times) / len(times)
    print(f"\n  Average latency: {avg_time:.2f}s ... ", end='')
    
    if avg_time < 3.0:
        print(f"{Colors.GREEN}✓ Meets standard (< 3s){Colors.NC}")
    else:
        print(f"{Colors.YELLOW}⚠ Exceeds target (>= 3s){Colors.NC}")
        # Performance warning does not count as test failure
    
    # Don't raise exception, performance test is for warning only


def main():
    """Main test flow"""
    print("=" * 50)
    print("Phase 1 Integration Tests (Python Version)")
    print("=" * 50)
    print()
    
    runner = TestRunner()
    
    # Check API service
    print("Step 1: Check API Service")
    print("-" * 50)
    
    try:
        requests.get(f"{API_BASE_URL}/health", timeout=2)
    except requests.exceptions.RequestException:
        print(f"{Colors.YELLOW}⚠ API service not running{Colors.NC}")
        print("Please run in another terminal: python3 src/api_server.py")
        print()
        input("Press Enter to continue after starting the service...")
        print()
    
    runner.run_test("Health check", test_health_check)
    print()
    
    # Test API endpoints
    print("Step 2: Test API Endpoints")
    print("-" * 50)
    runner.run_test("POST /optimize (min_stations)", test_optimize_min_stations)
    print()
    
    # Test different work orders
    print("Step 3: Test Different Work Orders")
    print("-" * 50)
    for wo in ["WO_A", "WO_B", "WO_C"]:
        runner.run_test(f"Optimize work order {wo}", test_optimize_work_order, wo)
    print()
    
    # Test different optimization objectives
    print("Step 4: Test Optimization Objectives")
    print("-" * 50)
    for goal in ["min_stations", "min_manpower", "min_idle"]:
        runner.run_test(f"Objective: {goal}", test_optimize_goal, goal)
    print()
    
    # Test other endpoints
    print("Step 5: Test Other Endpoints")
    print("-" * 50)
    runner.run_test("GET /workstations", test_workstations_endpoint)
    runner.run_test("GET /takt-summary", test_takt_summary_endpoint)
    runner.run_test("GET / (Dashboard)", test_dashboard_endpoint)
    runner.run_test("GET /api/docs (Swagger)", test_swagger_docs)
    print()
    
    # Performance test
    print("Step 6: Performance Test")
    print("-" * 50)
    runner.run_test("API latency (average of 3 runs)", test_performance)
    print()
    
    # Error handling tests
    print("Step 7: Error Handling Tests")
    print("-" * 50)
    runner.run_test("Invalid work order ID (should return 400)", test_invalid_work_order)
    runner.run_test("Invalid optimization goal (should return 400)", test_invalid_goal)
    runner.run_test("Negative takt time (should return 422)", test_negative_takt)
    print()
    
    # Print summary
    return runner.print_summary()


if __name__ == "__main__":
    sys.exit(main())
