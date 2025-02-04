# import pytest
# from profiler.core import Profiler
# import asyncio

# def test_profiler():
#     profiler = Profiler()

#     @profiler.track_performance
#     def sample_function():
#         a = [i for i in range(1000000)]
#         return sum(a)

#     @profiler.track_performance_async
#     async def sample_async_function():
#         await asyncio.sleep(1)
#         return "Done"

#     sample_function()
#     asyncio.run(sample_async_function())

#     function_data = profiler.get_function_data()
#     assert len(function_data) == 2

import unittest
from unittest.mock import patch
from profiler.core import Profiler
import os
import json

class TestProfiler(unittest.TestCase):
    def setUp(self):
        self.test_report_dir = "/tmp/profiler_test_reports"
        self.profiler = Profiler(report_dir=self.test_report_dir)
        
    def tearDown(self):
        for f in [os.path.join(self.test_report_dir, "JsonData", n) 
                for n in ["profiler_log.json", "profiler_time_series.json"]]:
            if os.path.exists(f):
                os.remove(f)
                
    def test_decorator(self):
        @self.profiler.track_memory
        def test_func():
            return "success"
            
        result = test_func()
        self.assertEqual(result, "success")
        
        # Verify data was recorded
        self.assertGreater(len(self.profiler.function_data), 0)
        
if __name__ == '__main__':
    unittest.main()
