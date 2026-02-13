/**
 * bot/utils/verifySignature.js
 *
 * Simple HMAC-based verification for incoming webhook payloads.
 * The CI workflow should include the same secret in the X-BOT-SIGN header or compute HMAC.
 *
 * Usage:
 *   const ok = verifySignature(req, process.env.BOTWEBHOOKSECRET);
 *
 * This function supports:
 *  - X-BOT-SIGN header containing the raw secret (simple equality) OR
 *  - X-Hub-Signature-256 header (sha256 HMAC of raw body) like GitHub style:
 *      'sha256=<hex>'
 *
 * Note: Express must be configured to provide raw body if using HMAC verification.
 */

const crypto = require('crypto');

function safeEqual(a, b) {
  try {
    const bufA = Buffer.from(a);
    const bufB = Buffer.from(b);
    if (bufA.length !== bufB.length) return false;
    return crypto.timingSafeEqual(bufA, bufB);
  } catch {
    return false;
  }
}

function verifySignature(req, secret) {
  if (!secret) return false;

  // 1) Simple header equality (X-BOT-SIGN)
  const headerSign = req.get('X-BOT-SIGN');
  if (headerSign && safeEqual(headerSign, secret)) return true;

  // 2) HMAC SHA256 (X-Hub-Signature-256) - expects raw body
  const hubSig = req.get('X-Hub-Signature-256') || req.get('X-Hub-Signature');
  if (hubSig && req.rawBody) {
    const sigParts = hubSig.split('=');
    const algo = sigParts.length === 2 ? sigParts[0] : 'sha256';
    const sig = sigParts.length === 2 ? sigParts[1] : sigParts[0];
    const hmac = crypto.createHmac('sha256', secret);
    hmac.update(req.rawBody);
    const digest = hmac.digest('hex');
    return safeEqual(digest, sig);
  }

  return false;
}

module.exports = verifySignature;
