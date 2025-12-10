/**
 * src/safe/propose.js
 *
 * CLI wrapper to submit proposals to a Safe Transaction Service.
 * Reads artifacts/safe-proposals.json and posts each payload to the Safe Transaction Service.
 * Writes artifacts/safe-proposals-result.json with returned safeTxHash and safeUrl for each proposal.
 */

const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

function readJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

function writeJson(p, obj) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, JSON.stringify(obj, null, 2));
}

async function postProposal(serviceUrl, safeAddress, payload) {
  // Safe Transaction Service API endpoint for creating a multisig transaction
  // Example: POST /api/v1/safes/{safeAddress}/multisig-transactions/
  const url = `${serviceUrl.replace(/\/$/, '')}/api/v1/safes/${safeAddress}/multisig-transactions/`;
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Safe service error ${res.status}: ${text}`);
  }
  return res.json();
}

async function submitSafeProposals(payloadPath, service, safe) {
  if (!fs.existsSync(payloadPath)) {
    console.error(`Payload file not found: ${payloadPath}`);
    throw new Error(`Payload file not found: ${payloadPath}`);
  }
  if (!service) {
    throw new Error('Safe transaction service URL not provided');
  }
  if (!safe) {
    throw new Error('Gnosis Safe address not provided');
  }

  const payload = readJson(payloadPath);
  const proposals = payload.proposals || [];
  if (!Array.isArray(proposals) || proposals.length === 0) {
    console.error('No proposals found in payload.');
    return;
  }

  const results = [];
  for (const p of proposals) {
    try {
      // Build body expected by Safe Transaction Service
      // Minimal fields: to, value, data, operation, safe
      const body = {
        to: p.to,
        value: p.value || '0',
        data: p.data,
        operation: p.operation || 0,
        safe: safe
      };

      console.log(`Proposing to Safe: to=${p.to} action=${p.action || 'unknown'}`);
      const resJson = await postProposal(service, safe, body);

      // The Safe service response shape can vary; capture common fields
      const safeTxHash = resJson.safeTxHash || resJson.transactionHash || resJson.txHash || null;
      const txId = resJson.txId || safeTxHash || null;
      const safeUrl = `${service.replace(/\/api.*$/, '')}/safes/${safe}/transactions/${txId || safeTxHash || ''}`;

      results.push({
        action: p.action || null,
        to: p.to,
        safeTxHash,
        txId,
        safeUrl,
        raw: resJson
      });

      // Small delay to avoid rate limits
      await new Promise(r => setTimeout(r, 500));
    } catch (err) {
      console.error('Proposal failed:', err.message || err);
      results.push({ action: p.action || null, to: p.to, error: err.message || String(err) });
    }
  }

  const outPath = path.join(__dirname, '..', '..', 'artifacts', 'safe-proposals-result.json');
  writeJson(outPath, { generatedAt: new Date().toISOString(), results });
  console.log(`Wrote results to ${outPath}`);
  return outPath;
}

module.exports = { submitSafeProposals };

// If run directly, execute with CLI args
if (require.main === module) {
  const minimist = require('minimist');
  const argv = minimist(process.argv.slice(2));

  const payloadPath = argv.payload || './artifacts/safe-proposals.json';
  const service = argv.service || process.env.SAFETXSERVICE_URL;
  const safe = argv.safe || process.env.GNOSISSAFEADDR;

  submitSafeProposals(payloadPath, service, safe).catch(err => {
    console.error(err);
    process.exit(1);
  });
}
