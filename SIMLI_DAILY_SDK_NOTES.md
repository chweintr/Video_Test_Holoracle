# Simli Daily SDK Implementation Notes
*Updated: 2025-08-13*

## Key Findings from Simli Support

### 1. Trinity Face Positioning Issue ⚠️
**Problem**: Trinity processing repositions/crops/outpaints faces, breaking our precise alignment requirements.

**Current Status**: 
- Confirmed by Simli team
- They're developing a "raw positioning mode" to maintain original image positioning
- No current workaround available
- Need to wait for Simli's fix

**Impact**: All custom faces will have positioning drift until fixed.

### 2. Custom Control Solution ✅
**Problem**: Need to trigger Simli sessions without the widget's built-in button.

**Solution**: Use Daily Client SDK directly
- Simli widgets use Daily Client SDK under the hood
- Can build completely custom interface with full control over:
  - Video positioning
  - Trigger buttons
  - Layout
  - Event handling

**Implementation**: See `simli_daily_custom.html` for proof of concept

### 3. Widget Sizing Constraints
**Current Limitations**:
- Widget trigger image cannot be same scale as widget
- Trigger cannot be positioned separately from widget
- Simli's internal styles override our sizing attempts

**Solutions**:
1. **Short-term**: Use MutationObserver to force sizing (implemented in main_kiosk.html)
2. **Long-term**: Move to Daily SDK for complete control

### 4. TTS API Key Issues
**Problem**: Adding `ttsAPIKey` to token request breaks all widgets (not just ElevenLabs ones)

**Clarifications from Simli**:
- API key should be added same format as simliAPIKey
- Should work for all agents (not conditional)
- Voice IDs are part of agent config (not request)

**Need to investigate**: Why tokens with ttsAPIKey fail to initialize widgets

### 5. Alpha Channel Support
**Status**: Not available
- WebRTC doesn't support alpha channels
- Custom backgrounds feature in development
- Current alpha masks are imperfect (being fixed)

## Daily SDK Implementation Strategy

### Architecture
```javascript
// Instead of:
<simli-widget agentid="xxx" />

// We use:
Daily SDK -> Custom Video Element -> Full Control
```

### Benefits
1. **Complete positioning control** - Video element can be placed anywhere
2. **Custom triggers** - Any UI element can start/stop sessions
3. **Better event handling** - Direct access to all WebRTC events
4. **No widget constraints** - No fighting with Simli's internal styles

### Implementation Steps
1. Get Simli session token from backend (same as current)
2. Create Daily call object with room URL
3. Join the room
4. Handle participant video tracks
5. Attach tracks to custom video element
6. Full control over sizing/positioning

### Required Backend Changes
The backend needs to return Daily room information:
```python
# Current response:
return {"token": simli_token}

# Needed response:
return {
    "token": simli_token,
    "roomUrl": daily_room_url,  # Need to extract this
    "sessionId": session_id
}
```

## Testing Checklist

### Immediate Tests
- [ ] Test `simli_daily_custom.html` with actual Simli tokens
- [ ] Verify Daily SDK can connect to Simli rooms
- [ ] Test video track attachment
- [ ] Verify avatar positioning control

### Integration Tests  
- [ ] Port Daily SDK to main_kiosk.html
- [ ] Test all 4 personas with Daily SDK
- [ ] Verify latency messages work with Daily events
- [ ] Test thinking indicators with Daily SDK

### Edge Cases
- [ ] Multiple persona switching
- [ ] Connection interruptions
- [ ] Browser compatibility
- [ ] Performance with 363x363 constraint

## File References

### Working Files
- `main_kiosk.html` - Current production version with widget
- `simli_daily_custom.html` - Daily SDK proof of concept
- `simli_voice_backend.py` - Backend that needs Daily room URL support

### Documentation
- Daily SDK: https://docs.daily.co/guides/products/client-sdk
- Simli Widget Source: Can be used as template for Daily implementation

## Next Steps

1. **Immediate**: Test if Daily SDK can connect to Simli rooms
2. **Short-term**: Update backend to return Daily room URLs
3. **Medium-term**: Port successful Daily implementation to main_kiosk.html
4. **Long-term**: Wait for Simli's Trinity positioning fix

## Contact
- Simli Support: Antony (SWE)
- Partnership discussions: Lars (CEO)
- Educational project collaboration potential noted