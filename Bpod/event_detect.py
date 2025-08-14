#!/usr/bin/env python3
"""
Bpod Port Event Monitor - Real-time using loop_handler()
"""

import queue
import time
from pybpodapi.protocol import Bpod
from pybpodapi.state_machine import StateMachine


class RealTimeBpodMonitor(Bpod):
    """
    Real-time Bpod event monitor using loop_handler() for immediate event processing.
    No threading needed - events are captured in real-time during state machine execution.
    """

    def __init__(self, serial_port=None, event_callback=None):
        """
        Initialize the monitor.
        
        Args:
            serial_port: Bpod serial port (None for auto-detect)
            event_callback: Function to call when events occur
        """
        super().__init__(serial_port=serial_port)
        self.event_callback = event_callback
        self.event_queue = queue.Queue()
        self.is_monitoring = False
        self._last_event_count = 0

        print(f"✓ Connected to Bpod on port: {self.serial_port}")

    def loop_handler(self):
        """
        Called continuously during state machine execution.
        This is where we capture events in real-time!
        """
        if not self.is_monitoring:
            return
            
        # Check if we have a current trial with events
        if hasattr(self.session, 'current_trial') and self.session.current_trial:
            current_trial = self.session.current_trial
            
            # Check if new events have been added since last check
            current_event_count = len(current_trial.events_occurrences)
            
            if current_event_count > self._last_event_count:
                # New events detected! Process them immediately
                new_events = current_trial.events_occurrences[self._last_event_count:]
                
                for event_obj in new_events:
                    self._process_realtime_event(event_obj)
                    
                self._last_event_count = current_event_count

    def _process_realtime_event(self, event_obj):
        """
        Process a single event immediately as it occurs.
        
        Args:
            event_obj: EventOccurrence object from Bpod
        """
        try:
            # Extract event information
            event_name = str(event_obj.event_name)

            # Skip timer events (Tup events)
            if 'Tup' in event_name or 'Timer' in event_name:
                return

            print(f"🔔 REAL-TIME EVENT: {event_name} at {time.time():.3f}")

            # Add to queue for main thread access
            self.event_queue.put(event_name)

            # Call user callback if provided
            if self.event_callback:
                try:
                    self.event_callback(event_name)
                except Exception as e:
                    print(f"❌ Error in event callback: {e}")

        except Exception as e:
            print(f"❌ Error processing real-time event: {e}")

    def start_monitoring(self, duration=None):
        """
        Start real-time monitoring using a single long-running state machine.
        
        Args:
            duration: How long to monitor (seconds). None for indefinite.
        """
        if self.is_monitoring:
            print("⚠️  Already monitoring!")
            return

        self.is_monitoring = True
        self._last_event_count = 0
        
        # Set timer duration
        if duration is None:
            timer_duration = 3600  # 1 hour default
        else:
            timer_duration = duration

        print(f"🚀 Starting real-time monitoring for {timer_duration}s...")

        # Create long-running state machine for continuous monitoring
        sma = StateMachine(self)

        # Single state that loops back on all events, exits on timer
        sma.add_state(
            state_name='Monitor',
            state_timer=timer_duration,  # Long monitoring period
            state_change_conditions={
                'Tup': 'exit',  # Exit when timer expires
                # Loop back to Monitor state on any port event
                'Port1In': 'Monitor', 'Port1Out': 'Monitor',
                'Port2In': 'Monitor', 'Port2Out': 'Monitor', 
                'Port3In': 'Monitor', 'Port3Out': 'Monitor',
                'Port4In': 'Monitor', 'Port4Out': 'Monitor',
                'Port5In': 'Monitor', 'Port5Out': 'Monitor',
                'Port6In': 'Monitor', 'Port6Out': 'Monitor',
                'Port7In': 'Monitor', 'Port7Out': 'Monitor',
                'Port8In': 'Monitor', 'Port8Out': 'Monitor',
                # Add BNC events
                'BNC1High': 'Monitor', 'BNC1Low': 'Monitor',
                'BNC2High': 'Monitor', 'BNC2Low': 'Monitor',
            },
            output_actions=[]
        )

        try:
            # Send and run the monitoring state machine
            self.send_state_machine(sma)
            self.run_state_machine(sma)  # This will call loop_handler() continuously
            
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
        except Exception as e:
            print(f"❌ Error during monitoring: {e}")
        finally:
            self.is_monitoring = False
            print("✅ Monitoring stopped")

    def stop_monitoring(self):
        """Stop the monitoring."""
        self.is_monitoring = False
        
    def get_recent_events(self, max_events=None):
        """
        Get recent events from the queue (non-blocking).
        
        Args:
            max_events: Maximum number of events to return
            
        Returns:
            List of event names
        """
        events = []
        count = 0

        while not self.event_queue.empty():
            if max_events and count >= max_events:
                break
            events.append(self.event_queue.get_nowait())
            count += 1

        return events

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup."""
        self.stop_monitoring()
        try:
            self.close()
        except:
            pass

def my_event_handler(event):
    """Custom event handler."""
    port_num = event[4]  # Extract port number
    action = 'ENTERED' if 'In' in event else 'EXITED'
    print(f"🐭 Port {port_num} {action} at {event}")

if __name__ == "__main__":
    try:
        # Example 1: Simple monitoring with real-time console output
        print("🔧 Starting simple real-time monitoring...")
        monitor = RealTimeBpodMonitor()
        monitor.start_monitoring(duration=30)  # Monitor for 30 seconds

    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        
    print("\n" + "="*50)
    
    try:
        # Example 2: Monitoring with custom event handler
        print("🔧 Starting monitoring with custom event handler...")
        monitor2 = RealTimeBpodMonitor(event_callback=my_event_handler)
        monitor2.start_monitoring(duration=30)  # Monitor for 30 seconds
        
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")  
    except Exception as e:
        print(f"❌ Error: {e}")

