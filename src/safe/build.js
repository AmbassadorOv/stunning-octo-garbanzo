/**
 * src/safe/build.js
 *
 * Reads a pinned manifest JSON and builds Safe proposal payloads for:
 *  - JuliusToken.mintTo(recipient, tokenId, metadataUri)
 *  - JuliusRegistry.register(juliusId, role, metadataUri, wallet)
 *
 * Writes artifacts/safe-proposals.json with an array of { to, value, data } entries.
 */

const fs = require('fs');
const path = require('path');
const { ethers } = require('ethers');

function readJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

function writeJson(p, obj) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, JSON.stringify(obj, null, 2));
}

function loadAbi(contractName) {
  // Expect Hardhat artifact path: artifacts/contracts/<Contract>.sol/<Contract>.json
  const artifactPath = path.join(__dirname, '..', '..', 'artifacts', 'contracts', `${contractName}.sol`, `${contractName}.json`);
  if (!fs.existsSync(artifactPath)) {
    throw new Error(`ABI artifact not found: ${artifactPath}`);
  }
  const artifact = readJson(artifactPath);
  return artifact.abi;
}

function encodeMintData(tokenAbi, recipient, tokenId, metadataUri) {
  const iface = new ethers.utils.Interface(tokenAbi);
  return iface.encodeFunctionData('mintTo', [recipient, tokenId, metadataUri]);
}

function encodeRegisterData(registryAbi, juliusId, role, metadataUri, wallet) {
  const iface = new ethers.utils.Interface(registryAbi);
  return iface.encodeFunctionData('register', [juliusId, role, metadataUri, wallet]);
}

async function buildSafeProposals(manifestPath) {
  if (!fs.existsSync(manifestPath)) {
    console.error(`Manifest not found: ${manifestPath}`);
    throw new Error(`Manifest not found: ${manifestPath}`);
  }

  const manifest = readJson(manifestPath);

  // Load ABIs
  const tokenAbi = loadAbi('JuliusToken');
  const registryAbi = loadAbi('JuliusRegistry');

  const proposals = [];

  // Determine default recipient (multisig) if present in manifest
  const defaultRecipient = (manifest.multisig && manifest.multisig.gnosissafe) || process.env.GNOSISSAFE_ADDR || null;

  // Build proposals for initial_mints if present
  if (manifest.nfts && Array.isArray(manifest.nfts.initial_mints)) {
    for (const mint of manifest.nfts.initial_mints) {
      const tokenId = mint.token_id;
      const metadata = mint.metadata;
      const juliusId = mint.julius_id || `JULIUS-${tokenId}`;
      const role = mint.role || mint.julius_id || 'Unknown';
      const recipient = mint.recipient || defaultRecipient;
      if (!recipient) {
        console.warn(`Skipping mint ${tokenId} because no recipient specified and no multisig found.`);
        continue;
      }

      // mintTo proposal
      const mintData = encodeMintData(tokenAbi, recipient, tokenId, metadata);
      proposals.push({
        action: 'mint',
        tokenId,
        juliusId,
        to: process.env.JULIUSTOKENADDR || manifest.contracts?.JuliusToken,
        value: '0',
        data: mintData
      });

      // register proposal (registry)
      const registryTo = process.env.JULIUSREGISTRYADDR || manifest.contracts?.JuliusRegistry;
      if (registryTo) {
        const regData = encodeRegisterData(registryAbi, juliusId, role, metadata, recipient);
        proposals.push({
          action: 'register',
          tokenId,
          juliusId,
          to: registryTo,
          value: '0',
          data: regData
        });
      }
    }
  }

  // Optionally build proposals for other registry updates in manifest.registries.initial_entries
  if (manifest.registries && Array.isArray(manifest.registries)) {
    for (const reg of manifest.registries) {
      if (reg.initialentries && reg.contractname === 'JuliusRegistry') {
        const registryTo = process.env.JULIUSREGISTRYADDR || manifest.contracts?.JuliusRegistry;
        for (const entry of reg.initial_entries) {
          const juliusId = entry.julius_id;
          const role = entry.role || 'Unknown';
          const metadataIpfs = entry.metadata_ipfs;
          const wallet = entry.wallet || defaultRecipient;
          if (!registryTo || !metadataIpfs || !juliusId) continue;
          const regData = encodeRegisterData(registryAbi, juliusId, role, metadataIpfs, wallet);
          proposals.push({
            action: 'register',
            juliusId,
            to: registryTo,
            value: '0',
            data: regData
          });
        }
      }
    }
  }

  // Write proposals artifact
  const outPath = path.join(__dirname, '..', '..', 'artifacts', 'safe-proposals.json');
  writeJson(outPath, { generatedAt: new Date().toISOString(), proposals });
  console.log(`Wrote ${proposals.length} proposal(s) to ${outPath}`);
  return outPath;
}

module.exports = { buildSafeProposals };

// If run directly, execute with CLI args
if (require.main === module) {
  const argv = require('minimist')(process.argv.slice(2));
  const manifestPath = argv.manifest || 'manifest/phase-zero-manifest.pinned.json';

  buildSafeProposals(manifestPath).catch(err => {
    console.error(err);
    process.exit(1);
  });
}
