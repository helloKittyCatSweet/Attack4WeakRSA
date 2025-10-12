import time
import threading
from concurrent.futures import ThreadPoolExecutor


class AttackWorker:
    """Multithreaded attack worker"""

    def __init__(self):
        self.found = False
        self.result = None
        self.attempts = 0
        self.lock = threading.Lock()
        self.start_time = None

    def multi_thread_attack(self, N, e, d0, X, M, exposure_type="MSB", num_threads=4, timeout=60):
        """Main multithreaded attack function"""
        print(f"\nStarting multithreaded attack:")
        print(f"  Exposure type: {exposure_type}")
        print(f"  Thread count: {num_threads}")
        print(f"  Time limit: {timeout} seconds")
        print(f"  Search space: 2^{X.bit_length() - 1}")

        # Reset state
        self.found = False
        self.result = None
        self.attempts = 0
        self.start_time = time.time()

        try:
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = self._start_workers(executor, num_threads, N, e, d0, X, M, exposure_type)
                self._wait_for_completion(futures, timeout)

        except TimeoutError:
            print(f"\nTime's up! Stopping search")
        except Exception as e:
            print(f"\nError: {e}")

        return self._finalize_attack()

    def _start_workers(self, executor, num_threads, N, e, d0, X, M, exposure_type):
        """Start worker threads"""
        futures = []
        if exposure_type == "MSB":
            for i in range(num_threads):
                future = executor.submit(self._msb_worker, i, num_threads, N, e, d0, X, M)
                futures.append(future)
        else:
            known_bits = d0.bit_length()
            for i in range(num_threads):
                future = executor.submit(self._lsb_worker, i, num_threads, N, e, d0, X, M, known_bits)
                futures.append(future)
        return futures

    def _msb_worker(self, thread_id, total_threads, N, e, d0, X, M, progress_interval=10000):
        """MSB exposure attack worker"""
        target = (1 - e * d0) % M
        local_attempts = 0

        for x in range(thread_id, X, total_threads):
            if self.found:
                return local_attempts

            if (e * x) % M == target:
                with self.lock:
                    if not self.found:
                        self.found = True
                        self.result = x
                        print(f"\nThread {thread_id} found solution!")
                return local_attempts

            local_attempts += 1
            self._report_progress(thread_id, local_attempts, progress_interval, X)

        with self.lock:
            self.attempts += local_attempts
        return local_attempts

    def _lsb_worker(self, thread_id, total_threads, N, e, d0, X, M, known_bits, progress_interval=10000):
        """LSB exposure attack worker"""
        local_attempts = 0

        for x in range(thread_id, X, total_threads):
            if self.found:
                return local_attempts

            d_candidate = (x << known_bits) + d0
            if (e * d_candidate - 1) % M == 0:
                with self.lock:
                    if not self.found:
                        self.found = True
                        self.result = x
                        print(f"\nThread {thread_id} found solution!")
                return local_attempts

            local_attempts += 1
            self._report_progress(thread_id, local_attempts, progress_interval, X)

        with self.lock:
            self.attempts += local_attempts
        return local_attempts

    def _report_progress(self, thread_id, local_attempts, progress_interval, X):
        """Report progress periodically"""
        if local_attempts % progress_interval == 0:
            with self.lock:
                self.attempts += local_attempts
                elapsed = time.time() - self.start_time
                if elapsed > 0:
                    speed = self.attempts / elapsed
                    eta = (X - self.attempts) / speed if speed > 0 else 0
                    print(
                        f"\rAttempts: {self.attempts:,} | Speed: {speed:,.0f}/sec | ETA: {eta:.1f}s | Thread {thread_id}",
                        end="", flush=True)

    def _wait_for_completion(self, futures, timeout):
        """Wait for worker completion"""
        for future in futures:
            if self.found:
                break
            future.result(timeout=timeout)

    def _finalize_attack(self):
        """Finalize attack and return results"""
        elapsed = time.time() - self.start_time

        print(f"\n\nAttack results:")
        print(f"  Total attempts: {self.attempts:,}")
        print(f"  Total time: {elapsed:.2f} seconds")
        if elapsed > 0:
            print(f"  Average speed: {self.attempts / elapsed:,.0f} attempts/sec")

        if self.found:
            print(f"  ✓ Successfully recovered private key!")
            return self.result
        else:
            print(f"  ✗ No solution found")
            return None