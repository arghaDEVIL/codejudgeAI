import { useState, useEffect, useRef, useCallback } from 'react';
import { WS_BASE_URL, getAuthToken } from '../utils/api';

/**
 * Custom hook for WebSocket connection to collaborative rooms
 * @param {string} roomCode - The room code to connect to
 * @param {boolean} enabled - Whether to connect (default: true)
 */
export const useWebSocket = (roomCode, enabled = true) => {
    const [connected, setConnected] = useState(false);
    const [connecting, setConnecting] = useState(false);
    const [error, setError] = useState(null);
    const [messages, setMessages] = useState([]);
    const [participants, setParticipants] = useState([]);
    const [roomState, setRoomState] = useState(null);

    const wsRef = useRef(null);
    const reconnectTimeoutRef = useRef(null);
    const reconnectAttemptsRef = useRef(0);
    const maxReconnectAttempts = 5;

    // Send message to WebSocket
    const sendMessage = useCallback((type, data) => {
        if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify({ type, data }));
            return true;
        }
        console.warn('WebSocket not connected, cannot send message');
        return false;
    }, []);

    // Send code change
    const sendCodeChange = useCallback((code, language = 'python') => {
        return sendMessage('code_change', { code, language, changes: [] });
    }, [sendMessage]);

    // Send cursor move
    const sendCursorMove = useCallback((position) => {
        return sendMessage('cursor_move', { position });
    }, [sendMessage]);

    // Send chat message
    const sendChatMessage = useCallback((message) => {
        return sendMessage('chat_message', { message });
    }, [sendMessage]);

    // Send ping
    const sendPing = useCallback(() => {
        return sendMessage('ping', {});
    }, [sendMessage]);

    // Connect to WebSocket
    const connect = useCallback(() => {
        if (!enabled || !roomCode) return;
        if (wsRef.current?.readyState === WebSocket.OPEN) return;

        const token = getAuthToken();
        if (!token) {
            setError('No authentication token found');
            return;
        }

        setConnecting(true);
        setError(null);

        const wsUrl = `${WS_BASE_URL}/ws/room/${roomCode}?token=${token}`;
        console.log('[WebSocket] Connecting to:', wsUrl);

        try {
            const ws = new WebSocket(wsUrl);

            ws.onopen = () => {
                console.log('[WebSocket] Connected');
                setConnected(true);
                setConnecting(false);
                setError(null);
                reconnectAttemptsRef.current = 0;
            };

            ws.onmessage = (event) => {
                try {
                    const message = JSON.parse(event.data);
                    console.log('[WebSocket] Received:', message.type);

                    // Handle different message types
                    switch (message.type) {
                        case 'room_state':
                            setRoomState(message.data);
                            setParticipants(message.data.participants || []);
                            break;

                        case 'user_joined':
                            setParticipants(prev => {
                                // Check if participant already exists
                                const exists = prev.some(p => p.user_id === message.data.user_id);
                                if (exists) {
                                    // Update existing participant
                                    return prev.map(p =>
                                        p.user_id === message.data.user_id ? message.data : p
                                    );
                                }
                                // Add new participant
                                return [...prev, message.data];
                            });
                            setMessages(prev => [...prev, {
                                type: 'system',
                                content: `${message.data.display_name} joined the room`,
                                timestamp: message.timestamp
                            }]);
                            break;

                        case 'user_left':
                            setParticipants(prev => prev.filter(p => p.user_id !== message.data.user_id));
                            setMessages(prev => [...prev, {
                                type: 'system',
                                content: `${message.data.display_name} left the room`,
                                timestamp: message.timestamp
                            }]);
                            break;

                        case 'code_update':
                            // Emit custom event for code updates
                            window.dispatchEvent(new CustomEvent('code_update', { detail: message.data }));
                            break;

                        case 'cursor_update':
                            // Emit custom event for cursor updates
                            window.dispatchEvent(new CustomEvent('cursor_update', { detail: message.data }));
                            break;

                        case 'chat_message':
                            setMessages(prev => [...prev, {
                                type: 'chat',
                                userId: message.data.user_id,
                                userName: message.data.user_name,
                                content: message.data.message,
                                timestamp: message.timestamp
                            }]);
                            break;

                        case 'error':
                            console.error('[WebSocket] Error:', message.data.message);
                            setError(message.data.message);
                            break;

                        case 'code_execution':
                            // Emit custom event for code execution results
                            window.dispatchEvent(new CustomEvent('code_execution', { detail: message.data }));
                            break;

                        case 'test_results':
                            // Emit custom event for test results
                            window.dispatchEvent(new CustomEvent('test_results', { detail: message.data }));
                            break;

                        case 'pong':
                            // Pong received, connection is alive
                            break;

                        default:
                            console.warn('[WebSocket] Unknown message type:', message.type);
                    }
                } catch (err) {
                    console.error('[WebSocket] Failed to parse message:', err);
                }
            };

            ws.onerror = (event) => {
                console.error('[WebSocket] Error:', event);
                setError('WebSocket connection error');
            };

            ws.onclose = (event) => {
                console.log('[WebSocket] Closed:', event.code, event.reason);
                setConnected(false);
                setConnecting(false);
                wsRef.current = null;

                // Attempt to reconnect if not a normal closure
                if (event.code !== 1000 && reconnectAttemptsRef.current < maxReconnectAttempts) {
                    const delay = Math.min(1000 * Math.pow(2, reconnectAttemptsRef.current), 10000);
                    console.log(`[WebSocket] Reconnecting in ${delay}ms...`);

                    reconnectTimeoutRef.current = setTimeout(() => {
                        reconnectAttemptsRef.current++;
                        connect();
                    }, delay);
                } else if (reconnectAttemptsRef.current >= maxReconnectAttempts) {
                    setError('Failed to reconnect after multiple attempts');
                }
            };

            wsRef.current = ws;
        } catch (err) {
            console.error('[WebSocket] Connection failed:', err);
            setError(err.message);
            setConnecting(false);
        }
    }, [roomCode, enabled]);

    // Disconnect from WebSocket
    const disconnect = useCallback(() => {
        if (reconnectTimeoutRef.current) {
            clearTimeout(reconnectTimeoutRef.current);
        }
        if (wsRef.current) {
            wsRef.current.close(1000, 'User disconnected');
            wsRef.current = null;
        }
        setConnected(false);
        setConnecting(false);
    }, []);

    // Connect on mount, disconnect on unmount
    useEffect(() => {
        if (enabled && roomCode) {
            connect();
        }

        return () => {
            disconnect();
        };
    }, [roomCode, enabled]);

    // Ping interval to keep connection alive
    useEffect(() => {
        if (!connected) return;

        const pingInterval = setInterval(() => {
            sendPing();
        }, 30000); // Ping every 30 seconds

        return () => clearInterval(pingInterval);
    }, [connected, sendPing]);

    return {
        connected,
        connecting,
        error,
        messages,
        participants,
        roomState,
        sendCodeChange,
        sendCursorMove,
        sendChatMessage,
        sendMessage,
        connect,
        disconnect,
    };
};

export default useWebSocket;
