import { useState, useEffect, useCallback, useRef } from 'react';

export interface VitalsReading {
  patient_id: string;
  hr: number;
  spo2: number;
  temp: number;
  bp_sys: number;
  bp_dia: number;
  risk_score: number;
  risk_label: string;
  timestamp: number;
}

export const useVitals = (url: string = import.meta.env.VITE_WS_URL || 'ws://localhost:8001/ws/vitals') => {
  const [vitals, setVitals] = useState<Record<string, VitalsReading>>({});
  const [isConnected, setIsConnected] = useState(false);
  const socketRef = useRef<WebSocket | null>(null);

  const connect = useCallback(() => {
    if (socketRef.current?.readyState === WebSocket.OPEN) return;

    const ws = new WebSocket(url);

    ws.onopen = () => {
      console.log('Connected to Vitals WebSocket');
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const data: VitalsReading = JSON.parse(event.data);
        setVitals((prev) => ({
          ...prev,
          [data.patient_id]: data,
        }));
      } catch (err) {
        console.error('Failed to parse vitals data:', err);
      }
    };

    ws.onclose = () => {
      console.log('Disconnected from Vitals WebSocket');
      setIsConnected(false);
      // Attempt reconnection after 3 seconds
      setTimeout(connect, 3000);
    };

    ws.onerror = (err) => {
      console.error('WebSocket error:', err);
      ws.close();
    };

    socketRef.current = ws;
  }, [url]);

  useEffect(() => {
    connect();
    return () => {
      socketRef.current?.close();
    };
  }, [connect]);

  return { vitals, isConnected };
};
