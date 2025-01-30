import pytest
from profiler.core import Profiler
import asyncio

def test_profiler():
    profiler = Profiler()

    @profiler.track_performance
    def sample_function():
        a = [i for i in range(1000000)]
        return sum(a)

    @profiler.track_performance_async
    async def sample_async_function():
        await asyncio.sleep(1)
        return "Done"

    sample_function()
    asyncio.run(sample_async_function())

    function_data = profiler.get_function_data()
    assert len(function_data) == 2
