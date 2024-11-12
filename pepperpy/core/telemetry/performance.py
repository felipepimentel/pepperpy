"""Performance monitoring implementation"""

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

import psutil


@dataclass
class ResourceUsage:
    """System resource usage information"""

    cpu_percent: float
    memory_percent: float
    disk_usage: Dict[str, float]
    network_io: Dict[str, int]
    timestamp: datetime


class PerformanceMonitor:
    """System performance monitor"""

    def __init__(self, interval: int = 5):
        self._interval = interval
        self._task = None
        self._running = False
        self._handlers = []
        self._history: List[ResourceUsage] = []
        self._max_history = 1000

    async def start(self) -> None:
        """Start performance monitoring"""
        self._running = True
        self._task = asyncio.create_task(self._monitor_loop())

    async def stop(self) -> None:
        """Stop performance monitoring"""
        self._running = False
        if self._task:
            await self._task

    def add_handler(self, handler: callable) -> None:
        """Add performance data handler"""
        self._handlers.append(handler)

    async def get_current_usage(self) -> ResourceUsage:
        """Get current resource usage"""
        try:
            # Get CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)

            # Get memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent

            # Get disk usage
            disk_usage = {}
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_usage[partition.mountpoint] = usage.percent
                except Exception:
                    continue

            # Get network I/O
            net_io = psutil.net_io_counters()
            network_io = {"bytes_sent": net_io.bytes_sent, "bytes_recv": net_io.bytes_recv}

            usage = ResourceUsage(
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                disk_usage=disk_usage,
                network_io=network_io,
                timestamp=datetime.utcnow(),
            )

            self._history.append(usage)
            if len(self._history) > self._max_history:
                self._history.pop(0)

            return usage

        except Exception as e:
            print(f"Failed to get resource usage: {str(e)}")
            return None

    async def get_history(self, limit: Optional[int] = None) -> List[ResourceUsage]:
        """Get usage history"""
        if limit:
            return self._history[-limit:]
        return self._history

    async def _monitor_loop(self) -> None:
        """Performance monitoring loop"""
        while self._running:
            try:
                usage = await self.get_current_usage()
                if usage:
                    for handler in self._handlers:
                        try:
                            await handler(usage)
                        except Exception as e:
                            print(f"Performance handler failed: {str(e)}")
            except Exception as e:
                print(f"Performance monitoring failed: {str(e)}")

            await asyncio.sleep(self._interval)
