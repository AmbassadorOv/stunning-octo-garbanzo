/**
 * src/anchor/orchestrator.js
 *
 * Translates the core logic from julius_anchor.py to JavaScript.
 * This module handles IPFS pinning, GitHub issue creation, and multi-platform notifications.
 */

const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

// --- Configuration & Setup ---
// These values are loaded from environment variables (.env file in development)
const CONFIG = {
    GITHUB_TOKEN: process.env.GITHUB_TOKEN,
    GITHUB_REPO: process.env.GITHUB_REPO,
    SLACK_WEBHOOK: process.env.SLACK_WEBHOOK,
    DISCORD_WEBHOOK: process.env.DISCORD_WEBHOOK,
    NFT_STORAGE_KEY: process.env.NFT_STORAGE_KEY,
};

const METADATA_DIR = "julius_metadata";
const BASE_IPFS_GATEWAY = "https://ipfs.io/ipfs/";

// Ensure metadata directory exists
if (!fs.existsSync(METADATA_DIR)) {
    fs.mkdirSync(METADATA_DIR);
}

/**
 * Generates JSON metadata and pins it to IPFS via NFT.Storage.
 * @param {object} roleData - The data for the role to be pinned.
 * @returns {Promise<string>} The IPFS CID of the pinned metadata.
 */
async function pinMetadata(roleData, logCallback) {
    if (!CONFIG.NFT_STORAGE_KEY) {
        logCallback("[ERROR] NFT_STORAGE_KEY is not configured.");
        return "CONFIGURATION_ERROR";
    }

    const metadata = {
        name: roleData.name,
        description: `Official Anchor Record for ${roleData.name}`,
        image: `ipfs://${roleData.image_cid || 'bafy_default_placeholder'}`,
        external_url: "https://julius.network",
        attributes: [
            { "trait_type": "Role", "value": roleData.name },
            { "trait_type": "ID", "value": roleData.id },
            { "trait_type": "Sync Date", "value": new Date().toISOString() },
            { "trait_type": "Anchor Status", "value": "Verified" }
        ]
    };

    const filePath = path.join(METADATA_DIR, `${roleData.id}.json`);
    fs.writeFileSync(filePath, JSON.stringify(metadata, null, 4));

    logCallback(`[IPFS] Uploading ${roleData.name}...`);
    try {
        const fileContent = fs.readFileSync(filePath);
        const response = await fetch('https://api.nft.storage/upload', {
            method: 'POST',
            headers: {
                "Authorization": `Bearer ${CONFIG.NFT_STORAGE_KEY}`,
                "Content-Type": "application/json"
            },
            body: fileContent
        });

        if (response.ok) {
            const result = await response.json();
            const cid = result.value.cid;
            logCallback(`[SUCCESS] Pinned at: ${cid}`);
            return cid;
        } else {
            const errorText = await response.text();
            logCallback(`[ERROR] IPFS Upload failed: ${errorText}`);
            return "HASH_GENERATION_FAILED";
        }
    } catch (e) {
        logCallback(`[ERROR] Connection error: ${e.message}`);
        return "CONNECTION_ERROR";
    }
}

/**
 * Creates a GitHub Issue to act as the permanent log of the action.
 * @param {string} title - The title of the GitHub issue.
 * @param {string} body - The body content of the GitHub issue.
 * @returns {Promise<string>} The URL of the created issue or "None".
 */
async function updateAnchorLog(title, body, logCallback) {
    if (!CONFIG.GITHUB_TOKEN || !CONFIG.GITHUB_REPO) {
        logCallback("[ERROR] GitHub token or repo is not configured.");
        return "None";
    }

    const url = `https://api.github.com/repos/${CONFIG.GITHUB_REPO}/issues`;
    const data = { title, body, labels: ["Julius-Anchor", "Automated"] };

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                "Authorization": `token ${CONFIG.GITHUB_TOKEN}`,
                "Accept": "application/vnd.github.v3+json"
            },
            body: JSON.stringify(data)
        });

        if (response.status === 201) {
            const issue = await response.json();
            const issueUrl = issue.html_url;
            logCallback(`[GITHUB] Logged to Anchor: ${issueUrl}`);
            return issueUrl;
        } else {
            const errorText = await response.text();
            logCallback(`[ERROR] GitHub logging failed: ${errorText}`);
            return "None";
        }
    } catch (e) {
        logCallback(`[ERROR] GitHub connection error: ${e.message}`);
        return "None";
    }
}

/**
 * Broadcasts the update to all connected platforms.
 * @param {string} message - The main message content.
 * @param {object} links - A dictionary of links to include.
 */
async function notifyPlatforms(message, links, logCallback) {
    let formatted_message = `**⚓ Julius Anchor Update**\n${message}\n`;
    for (const [key, value] of Object.entries(links)) {
        formatted_message += `- ${key}: ${value}\n`;
    }

    // Slack
    if (CONFIG.SLACK_WEBHOOK && CONFIG.SLACK_WEBHOOK.includes('hooks.slack.com')) {
        await fetch(CONFIG.SLACK_WEBHOOK, { method: 'POST', body: JSON.stringify({ text: formatted_message.replace(/\*\*/g, "*") }) });
        logCallback("[SLACK] Notification sent.");
    }

    // Discord
    if (CONFIG.DISCORD_WEBHOOK && CONFIG.DISCORD_WEBHOOK.includes('discord.com/api')) {
        await fetch(CONFIG.DISCORD_WEBHOOK, { method: 'POST', body: JSON.stringify({ content: formatted_message }) });
        logCallback("[DISCORD] Notification sent.");
    }
}

/**
 * The main workflow runner for the Anchor system.
 * @param {function} logCallback - A function to call for logging updates.
 */
async function runSyncCycle(logCallback) {
    logCallback(`🌊 STARTING JULIUS ANCHOR SYNC: ${new Date()}`);

    // In the future, this list can be fetched from a database or API
    const active_roles = [
        { "id": "001", "name": "Julius_Prime", "image_cid": "bafybeig..." },
        { "id": "002", "name": "Treasury_Bot", "image_cid": "bafybeic..." },
        { "id": "003", "name": "Bridge_Operator", "image_cid": "bafybeid..." }
    ];

    const logs = [];
    for (const role of active_roles) {
        const cid = await pinMetadata(role, logCallback);
        logs.push(`| ${role.name} | \`${cid}\` |`);
    }

    // Create Central Log Body
    let logBody = "### Julius Metadata Sync Report\n\nThe following entities have been anchored to IPFS and validated.\n\n";
    logBody += "| Entity | IPFS CID |\n|---|---|\n" + logs.join("\n");

    // Push to Anchor (GitHub)
    const issueUrl = await updateAnchorLog(`Anchor Sync: ${new Date().toISOString().split('T')[0]}`, logBody, logCallback);

    // Notify Teams
    if (issueUrl !== "None") {
        await notifyPlatforms(
            `New metadata sync completed for ${active_roles.length} entities.`,
            { "GitHub Log": issueUrl, "IPFS Gateway": BASE_IPFS_GATEWAY },
            logCallback
        );
    }

    logCallback("✅ SYNC COMPLETE.");
}

module.exports = { runSyncCycle };
