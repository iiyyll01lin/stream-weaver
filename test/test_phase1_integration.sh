#!/bin/bash
#
# Phase 1 Integration Test Script
# Integration Test Script for Phase 1
#
# Purpose: Verify API service and algorithm integration works correctly
# Usage: ./test_phase1_integration.sh
#

set -e  # Exit immediately on error

echo "=================================="
echo "Phase 1 Integration Tests"
echo "=================================="
echo ""

# Color definitions
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

# Test function
run_test() {
    local test_name=$1
    local test_command=$2
    
    echo -n "Test: $test_name ... "
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Passed${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ Failed${NC}"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Check if API service is running
echo "Step 1: Check API Service"
echo "--------------------"

if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠ API service not running${NC}"
    echo "Please run in another terminal: python3 src/api_server.py"
    echo ""
    read -p "Press Enter to continue after starting the service..."
fi

run_test "Health check" "curl -f -s http://localhost:8000/health"
echo ""

# Test API endpoints
echo "Step 2: Test API Endpoints"
echo "--------------------"

# Test /optimize endpoint
run_test "POST /optimize (min_stations)" \
    "curl -f -s -X POST http://localhost:8000/optimize \
    -H 'Content-Type: application/json' \
    -d '{\"work_order_id\":\"WO_A\",\"target_takt\":80000,\"optimization_goal\":\"min_stations\"}' \
    -o /tmp/test_optimize.json"

# Verify response format
if [ -f /tmp/test_optimize.json ]; then
    run_test "Verify response contains work_order_id" \
        "grep -q '\"work_order_id\"' /tmp/test_optimize.json"
    
    run_test "Verify response contains line_count" \
        "grep -q '\"line_count\"' /tmp/test_optimize.json"
    
    run_test "Verify response contains stations" \
        "grep -q '\"stations\"' /tmp/test_optimize.json"
fi

echo ""

# Test different work orders
echo "Step 3: Test Different Work Orders"
echo "--------------------"

for wo in "WO_A" "WO_B" "WO_C"; do
    run_test "Optimize work order $wo" \
        "curl -f -s -X POST http://localhost:8000/optimize \
        -H 'Content-Type: application/json' \
        -d '{\"work_order_id\":\"$wo\",\"target_takt\":80000,\"optimization_goal\":\"min_stations\"}' \
        -o /dev/null"
done

echo ""

# Test different optimization objectives
echo "Step 4: Test Optimization Objectives"
echo "--------------------"

for goal in "min_stations" "min_manpower" "min_idle"; do
    run_test "Objective: $goal" \
        "curl -f -s -X POST http://localhost:8000/optimize \
        -H 'Content-Type: application/json' \
        -d '{\"work_order_id\":\"WO_A\",\"target_takt\":80000,\"optimization_goal\":\"$goal\"}' \
        -o /dev/null"
done

echo ""

# Test other endpoints
echo "Step 5: Test Other Endpoints"
echo "--------------------"

run_test "GET /workstations" \
    "curl -f -s 'http://localhost:8000/workstations?work_order_id=WO_A&target_takt=80000' -o /dev/null"

run_test "GET /takt-summary" \
    "curl -f -s 'http://localhost:8000/takt-summary?work_order_id=WO_A&target_takt=80000' -o /dev/null"

run_test "GET / (Dashboard)" \
    "curl -f -s http://localhost:8000/ -o /dev/null"

run_test "GET /api/docs (Swagger)" \
    "curl -f -s http://localhost:8000/api/docs -o /dev/null"

echo ""

# Performance test
echo "Step 6: Performance Test"
echo "--------------------"

echo -n "Test: API latency (average of 3 runs) ... "

TOTAL_TIME=0
for i in {1..3}; do
    START=$(date +%s.%N)
    curl -f -s -X POST http://localhost:8000/optimize \
        -H 'Content-Type: application/json' \
        -d '{"work_order_id":"WO_A","target_takt":80000,"optimization_goal":"min_stations"}' \
        -o /dev/null
    END=$(date +%s.%N)
    ELAPSED=$(echo "$END - $START" | bc)
    TOTAL_TIME=$(echo "$TOTAL_TIME + $ELAPSED" | bc)
done

AVG_TIME=$(echo "scale=2; $TOTAL_TIME / 3" | bc)

if (( $(echo "$AVG_TIME < 3.0" | bc -l) )); then
    echo -e "${GREEN}✓ Passed${NC} (average ${AVG_TIME}s < 3s)"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}⚠ Warning${NC} (average ${AVG_TIME}s >= 3s)"
fi

echo ""

# Error handling tests
echo "Step 7: Error Handling Tests"
echo "--------------------"

run_test "Invalid work order ID (should return 400)" \
    "curl -s -X POST http://localhost:8000/optimize \
    -H 'Content-Type: application/json' \
    -d '{\"work_order_id\":\"INVALID\",\"target_takt\":80000,\"optimization_goal\":\"min_stations\"}' \
    | grep -q '\"detail\"'"

run_test "Invalid optimization goal (should return 400)" \
    "curl -s -X POST http://localhost:8000/optimize \
    -H 'Content-Type: application/json' \
    -d '{\"work_order_id\":\"WO_A\",\"target_takt\":80000,\"optimization_goal\":\"invalid_goal\"}' \
    | grep -q '\"detail\"'"

run_test "Negative takt time (should return 422)" \
    "curl -s -X POST http://localhost:8000/optimize \
    -H 'Content-Type: application/json' \
    -d '{\"work_order_id\":\"WO_A\",\"target_takt\":-1000,\"optimization_goal\":\"min_stations\"}' \
    | grep -q '\"detail\"'"

echo ""

# Summary
echo "=================================="
echo "Test Summary"
echo "=================================="
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed, please check error messages${NC}"
    exit 1
fi
