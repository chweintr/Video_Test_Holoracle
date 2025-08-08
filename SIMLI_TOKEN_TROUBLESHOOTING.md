# 🔧 Simli Token Generation Troubleshooting Guide

## 🚨 Current Issue: 422 Errors on Token Generation

**Error Pattern**: Getting 422 (Unprocessable Entity) when requesting `/simli-token?persona=X`

## 📋 What We've Tried and Outcomes

### ❌ Attempt 1: Add simliAPIKey to request body
- **Change**: Added `simliAPIKey` to JSON body, removed from header
- **Result**: Still 401 Unauthorized
- **Commit**: d13e94e

### ❌ Attempt 2: Remove agentId parameter  
- **Change**: Only send `{"simliAPIKey": api_key}` based on web documentation
- **Result**: API worked but frontend still failed
- **Commit**: 07e61a6

### ❌ Attempt 3: Revert to original working format
- **Change**: Back to `Authorization: Bearer` + `{"agentId": agent_id}`
- **Result**: Still 422 errors locally and on Railway
- **Commit**: 99d5671

## 🔍 Git History Analysis

**Working Version**: Commit `8aeb805` (feat: add /simli-token endpoint)
```python
# Original working format:
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
json = {"agentId": agent_id}
```

**When it broke**: After we started modifying the API format without testing each change thoroughly.

## 🧪 API Testing Results

### Format 1: Bearer + agentId (Original)
```bash
curl -X POST "https://api.simli.ai/createE2ESessionToken" \
  -H "Authorization: Bearer n0dougxadvdi4hf7poa4xn" \
  -H "Content-Type: application/json" \
  -d '{"agentId": "6926a39d-638b-49c5-9328-79efa034e9a4"}'
```
**Result**: ???

### Format 2: simliAPIKey in body only
```bash 
curl -X POST "https://api.simli.ai/createE2ESessionToken" \
  -H "Content-Type: application/json" \
  -d '{"simliAPIKey": "n0dougxadvdi4hf7poa4xn"}'
```
**Result**: ✅ Returns `{"session_token": "..."}`

### Format 3: Both methods combined
```bash
curl -X POST "https://api.simli.ai/createE2ESessionToken" \
  -H "Authorization: Bearer n0dougxadvdi4hf7poa4xn" \
  -H "Content-Type: application/json" \
  -d '{"agentId": "6926a39d-638b-49c5-9328-79efa034e9a4", "simliAPIKey": "n0dougxadvdi4hf7poa4xn"}'
```
**Result**: ???

## 🔑 Environment Variables Status

### Local (.env file):
- ✅ `SIMLI_API_KEY=n0dougxadvdi4hf7poa4xn`
- ✅ `OPENAI_API_KEY=sk-proj-...iFEA`
- ✅ `ELEVENLABS_API_KEY=sk_439d393c...`

### Railway (Environment Variables):
- ❓ `SIMLI_API_KEY` - present but needs verification
- ❓ `OPENAI_API_KEY` - present but needs verification
- ❓ Possible duplicates with trailing spaces

## 🎯 Next Debugging Steps

1. **Test each API format directly** against Simli API to see which works
2. **Check Railway environment variables** for duplicates/spaces
3. **Test token generation locally** with working server
4. **Compare exact request/response** between local and Railway
5. **Check if API key itself is valid** on Simli dashboard

## 🚀 Working Configurations Archive

### When System Was Working:
- **Date**: Around commit 8aeb805
- **API Format**: Bearer token + agentId
- **Environment**: Local development
- **Status**: Personas were switching successfully

### Current Status:
- **Date**: Current session
- **API Format**: Tried multiple variations
- **Environment**: Both local and Railway failing
- **Status**: 422 errors across all personas

## 💡 Possible Root Causes

1. **API Key Changed**: Simli may have invalidated the old key
2. **API Format Changed**: Simli may have updated their API requirements
3. **Environment Issues**: Railway variables corrupted/duplicated
4. **Network Issues**: Firewall/proxy blocking requests
5. **Rate Limiting**: Too many failed attempts causing temporary ban

## ✅ WORKING SOLUTION (CONFIRMED)

**Tested and working as of current session:**

```python
# WORKING CONFIGURATION:
url = "https://api.simli.ai/createE2ESessionToken"
headers = {
    "Content-Type": "application/json"
}
json_body = {
    "simliAPIKey": api_key  # ONLY this field needed
}

# Response format:
{
  "session_token": "gAAAAAB..."  # Long encrypted token
}

# Token extraction:
token = response_data.get("session_token")
```

**Why previous attempts failed:**
- ❌ `Authorization: Bearer` header is NOT needed
- ❌ `agentId` parameter causes 422 error ("simliAPIKey field required")
- ❌ The original "working" format was never actually working

**The 422 error was telling us exactly what was wrong**: Missing `simliAPIKey` field in request body.

## 🔄 Update Process

**IMPORTANT**: Every time we solve a token issue:
1. ✅ Document the exact working configuration above
2. ✅ Update this troubleshooting guide
3. ✅ Commit changes with clear description
4. ✅ Test on both local and Railway
5. ✅ Update PROJECT_CONTEXT.md with current status

---
*Last Updated*: Current debugging session
*Status*: 422 errors across all environments - investigation ongoing