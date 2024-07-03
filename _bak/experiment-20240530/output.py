W 00:32:22    HolonicAgent:137  signal_handler) 65d5> <Client1> Ctrl-C: Client1

(entkm) D:\Work\NCU\投搞\SEC\experiment>python many_to_one.py
I 00:32:24     many_to_one:104        <module>) ***** ManyToOneControl start *****
D 00:32:24    HolonicAgent:148      _run_begin) e353> Create broker
I 00:32:24     mqtt_broker:042           start) MQTT broker is starting...
D 00:32:24    HolonicAgent:148      _run_begin) b55e> Create broker
I 00:32:24     mqtt_broker:042           start) MQTT broker is starting...
I 00:32:24     mqtt_broker:023     _on_connect) MQTT broker connected. url: localhost, port: 1884, keepalive: 60
D 00:32:24    HolonicAgent:155      _run_begin) e353> start interval_loop
I 00:32:24    HolonicAgent:297     _on_connect) e353> <ManyToOne> Broker is connected.
D 00:32:24    HolonicAgent:148      _run_begin) c3f2> Create broker
I 00:32:24     mqtt_broker:042           start) MQTT broker is starting...
D 00:32:24    HolonicAgent:148      _run_begin) a979> Create broker
I 00:32:24     mqtt_broker:042           start) MQTT broker is starting...
D 00:32:24    HolonicAgent:148      _run_begin) d7f5> Create broker
I 00:32:24     mqtt_broker:042           start) MQTT broker is starting...
D 00:32:24    HolonicAgent:148      _run_begin) 28f4> Create broker
I 00:32:24     mqtt_broker:042           start) MQTT broker is starting...
D 00:32:24    HolonicAgent:155      _run_begin) b55e> start interval_loop
D 00:32:24    HolonicAgent:155      _run_begin) c3f2> start interval_loop
I 00:32:24     mqtt_broker:023     _on_connect) MQTT broker connected. url: localhost, port: 1884, keepalive: 60
I 00:32:24     mqtt_broker:023     _on_connect) MQTT broker connected. url: localhost, port: 1884, keepalive: 60
I 00:32:24    HolonicAgent:297     _on_connect) b55e> <Reporter> Broker is connected.
I 00:32:24    HolonicAgent:297     _on_connect) c3f2> <Client1> Broker is connected.
D 00:32:24    HolonicAgent:271 set_topic_handler) b55e> Set topic handler: report.elapsed
D 00:32:24    HolonicAgent:271 set_topic_handler) c3f2> Set topic handler: service1.resp
Request: c3f2-0
D 00:32:24    HolonicAgent:155      _run_begin) a979> start interval_loop
I 00:32:24     mqtt_broker:023     _on_connect) MQTT broker connected. url: localhost, port: 1884, keepalive: 60
I 00:32:24    HolonicAgent:297     _on_connect) a979> <Client1> Broker is connected.
D 00:32:24    HolonicAgent:271 set_topic_handler) a979> Set topic handler: service1.resp
Request: a979-0
D 00:32:24    HolonicAgent:155      _run_begin) d7f5> start interval_loop
I 00:32:24     mqtt_broker:023     _on_connect) MQTT broker connected. url: localhost, port: 1884, keepalive: 60
D 00:32:24    HolonicAgent:148      _run_begin) 5e25> Create broker
I 00:32:24    HolonicAgent:297     _on_connect) d7f5> <Service1> Broker is connected.
I 00:32:24     mqtt_broker:042           start) MQTT broker is starting...
D 00:32:24    HolonicAgent:271 set_topic_handler) d7f5> Set topic handler: service1
D 00:32:24    HolonicAgent:155      _run_begin) 28f4> start interval_loop
I 00:32:24     mqtt_broker:023     _on_connect) MQTT broker connected. url: localhost, port: 1884, keepalive: 60
I 00:32:24    HolonicAgent:297     _on_connect) 28f4> <Client1> Broker is connected.
D 00:32:24    HolonicAgent:271 set_topic_handler) 28f4> Set topic handler: service1.resp
Request: 28f4-0
D 00:32:24    HolonicAgent:148      _run_begin) 589f> Create broker
I 00:32:24     mqtt_broker:042           start) MQTT broker is starting...
D 00:32:24    HolonicAgent:155      _run_begin) 5e25> start interval_loop
I 00:32:24     mqtt_broker:023     _on_connect) MQTT broker connected. url: localhost, port: 1884, keepalive: 60
I 00:32:24    HolonicAgent:297     _on_connect) 5e25> <Client1> Broker is connected.
D 00:32:24    HolonicAgent:271 set_topic_handler) 5e25> Set topic handler: service1.resp
Request: 5e25-0
D 00:32:24    HolonicAgent:155      _run_begin) 589f> start interval_loop
I 00:32:24     mqtt_broker:023     _on_connect) MQTT broker connected. url: localhost, port: 1884, keepalive: 60
I 00:32:24    HolonicAgent:297     _on_connect) 589f> <Client1> Broker is connected.
D 00:32:24    HolonicAgent:271 set_topic_handler) 589f> Set topic handler: service1.resp
Request: 589f-0
Responsed: 28f4-0
Responsed: 5e25-0
Responsed: 589f-0
Request: 5e25-1
Responsed: 5e25-1
Request: c3f2-1
Responsed: c3f2-1
Request: 28f4-1
Responsed: 28f4-1
Request: 589f-1
Request: a979-1
Responsed: a979-1Responsed: 589f-1

Request: a979-2
Responsed: a979-2
Request: 28f4-2
Responsed: 28f4-2
Request: 589f-2
Responsed: 589f-2
Request: 5e25-2
Responsed: 5e25-2
Request: c3f2-2
Responsed: c3f2-2
Request: a979-3
Responsed: a979-3
Request: 28f4-3
Responsed: 28f4-3
Request: 5e25-3
Responsed: 5e25-3
Request: 589f-3
Responsed: 589f-3
Request: a979-4
Request: c3f2-3
Responsed: a979-4
Responsed: c3f2-3
Request: 5e25-4
Responsed: 5e25-4
Request: 28f4-4
Responsed: 28f4-4
Request: 589f-4
Request: a979-5
Responsed: 589f-4
Responsed: a979-5
Request: 28f4-5
Responsed: 28f4-5
Request: c3f2-4
Responsed: c3f2-4
Request: 5e25-5
Responsed: 5e25-5
Request: 28f4-6
Responsed: 28f4-6
Request: a979-6
Responsed: a979-6
Request: 589f-5
Responsed: 589f-5
Request: c3f2-5
Responsed: c3f2-5
Request: 5e25-6
Responsed: 5e25-6
Request: 28f4-7
Responsed: 28f4-7
Request: 589f-6
Responsed: 589f-6
Request: a979-7
Responsed: a979-7
Request: 5e25-7
Responsed: 5e25-7
Request: c3f2-6
Responsed: c3f2-6
Request: a979-8
Responsed: a979-8
Request: 28f4-8
Responsed: 28f4-8
Request: 5e25-8Request: 589f-7

Responsed: 5e25-8
Responsed: 589f-7
Request: a979-9
Responsed: a979-9
Request: c3f2-7
Responsed: c3f2-7
Request: 5e25-9
Responsed: 5e25-9
[5e25] Average elapsed time: 19.169282913208008 ms
elapsed_milis: 19.169282913208008, len: 0, total_clients: 5
Request: 589f-8
Responsed: 589f-8
Request: c3f2-8
Responsed: c3f2-8
Request: 28f4-9
Responsed: 28f4-9
[28f4] Average elapsed time: 18.31843852996826 ms
elapsed_milis: 18.31843852996826, len: 1, total_clients: 5
Request: 589f-9
Responsed: 589f-9
[589f] Average elapsed time: 24.616622924804688 ms
elapsed_milis: 24.616622924804688, len: 2, total_clients: 5
Request: c3f2-9
Responsed: c3f2-9