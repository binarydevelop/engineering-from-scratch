#!/usr/bin/env python3
def calculate_buffer_dynamics(prod_rate=10000, cons_rate=8000, duration_sec=3600, record_bytes=1024):
    print("--- Queueing & Buffer Capacity Analysis ---")
    print(f"Production Rate: {prod_rate:,} msgs/s")
    print(f"Consumer Rate:   {cons_rate:,} msgs/s")
    print(f"Duration:        {duration_sec/60:.0f} minutes\n")

    net_rate = prod_rate - cons_rate
    accumulated_msgs = net_rate * duration_sec
    accumulated_mb = (accumulated_msgs * record_bytes) / (1024 * 1024)

    print(f"Backlog Accumulation Rate: +{net_rate:,} msgs/s")
    print(f"Total Accumulated Backlog:  {accumulated_msgs:,} records")
    print(f"Storage Buffer Required:    {accumulated_mb:,.1f} MB ({accumulated_mb/1024:.2f} GB)\n")

    # Catch up calculation if consumer scales to 15,000/s
    scaled_cons_rate = 15000
    recovery_rate = scaled_cons_rate - prod_rate
    catch_up_sec = accumulated_msgs / recovery_rate
    print(f"If consumer capacity is scaled to {scaled_cons_rate:,} msgs/s:")
    print(f" -> Drain Rate: {recovery_rate:,} msgs/s")
    print(f" -> Time to drain backlog completely: {catch_up_sec/60:.1f} minutes")

if __name__ == "__main__":
    calculate_buffer_dynamics()
