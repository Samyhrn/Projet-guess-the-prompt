"use strict";
var _a;
exports.__esModule = true;
var node_fetch_1 = require("node-fetch");
var node_fs_1 = require("node:fs");
var engineId = 'stable-diffusion-v1-5';
var apiHost = (_a = process.env.API_HOST) !== null && _a !== void 0 ? _a : 'https://api.stability.ai';
var apiKey = process.env.STABILITY_API_KEY;
if (!apiKey)
    throw new Error('Missing Stability API key.');
var response = await (0, node_fetch_1["default"])("".concat(apiHost, "/v1/generation/").concat(engineId, "/text-to-image"), {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
        Authorization: "Bearer ".concat(apiKey)
    },
    body: JSON.stringify({
        text_prompts: [
            {
                text: 'A lighthouse on a cliff'
            },
        ],
        cfg_scale: 7,
        clip_guidance_preset: 'FAST_BLUE',
        height: 512,
        width: 512,
        samples: 1,
        steps: 30
    })
});
if (!response.ok) {
    throw new Error("Non-200 response: ".concat(await response.text()));
}
var responseJSON = (await response.json());
responseJSON.artifacts.forEach(function (image, index) {
    node_fs_1["default"].writeFileSync("./out/v1_txt2img_".concat(index, ".png"), Buffer.from(image.base64, 'base64'));
});
