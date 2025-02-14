import { readFile, writeFile } from 'fs/promises'; // 使用 fs/promises 进行异步操作
import path from 'path';
import WebSocket from "ws";
import readline from "readline"; // Import readline module for interactive input
import fs from 'fs';
import decodeAudio from 'audio-decode';
//import HttpsProxyAgent from 'https-proxy-agent';
import { HttpsProxyAgent } from 'https-proxy-agent';

// 创建代理代理对象
const proxyUrl = 'http://127.0.0.1:7890'; // 替换为你的代理地址
const agent = new HttpsProxyAgent(proxyUrl);

const url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01";

// Set up readline interface for interactive input
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function floatTo16BitPCM(float32Array) {
    const buffer = new ArrayBuffer(float32Array.length * 2);
    const view = new DataView(buffer);
    let offset = 0;
    for (let i = 0; i < float32Array.length; i++, offset += 2) {
      let s = Math.max(-1, Math.min(1, float32Array[i]));
      view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true);
    }
    return buffer;
  }

  // Converts a Float32Array to base64-encoded PCM16 data
function base64EncodeAudio(float32Array) {
    const arrayBuffer = floatTo16BitPCM(float32Array);
    let binary = '';
    let bytes = new Uint8Array(arrayBuffer);
    const chunkSize = 0x8000; // 32KB chunk size
    for (let i = 0; i < bytes.length; i += chunkSize) {
      let chunk = bytes.subarray(i, i + chunkSize);
      binary += String.fromCharCode.apply(null, chunk);
    }
    return btoa(binary);
}

function init_socket(){
    // const ws =  new WebSocket(url, {
    //     agent: agent,
    //     headers: {
    //         //"Authorization": "Bearer sk-REd5NJgvu7tMGVb95a5c99BcE5D0447993D7B987023bF896",
    //         "Authorization": "Bearer sk-svcacct-Wrf-AdxS-NdcC4cEITLLLaGT2EAFuofef36dVGxA-H0HPbZ-SvXN3O-jSPYT3BlbkFJ8-eUD0P_yvJzRRZ3z0mMELlXKPSS4Cms5pH0yw4ieQLtA9HR4ldNFc8rooAA",
    //         "OpenAI-Beta": "realtime=v1",
    //     },
    //     //rejectUnauthorized: false
    // });
    // ws.on("open", function open() {
    //     console.log("Connected to server.");
    //
    //     // Send an initial response creation message
    //     ws.send(JSON.stringify({
    //         type: "response.create",
    //         response: {
    //             modalities: ["text"],
    //             instructions: "Please assist the user.",
    //         }
    //     }));
    // });
    return new Promise((resolve, reject) => {
        const ws =  new WebSocket(url, {
        agent: agent,
        headers: {
            //"Authorization": "Bearer sk-REd5NJgvu7tMGVb95a5c99BcE5D0447993D7B987023bF896",
            "Authorization": "Bearer sk-svcacct-Wrf-AdxS-NdcC4cEITLLLaGT2EAFuofef36dVGxA-H0HPbZ-SvXN3O-jSPYT3BlbkFJ8-eUD0P_yvJzRRZ3z0mMELlXKPSS4Cms5pH0yw4ieQLtA9HR4ldNFc8rooAA",
            "OpenAI-Beta": "realtime=v1",
        },
        //rejectUnauthorized: false
        });

        ws.on("open", () => {
            console.log("WebSocket connection opened.");
            resolve(ws); // 连接成功，解析 Promise
        });

        ws.on("open", function open() {
            console.log("Connected to server.");

            // Send an initial response creation message
            ws.send(JSON.stringify({
                type: "response.create",
                response: {
                    modalities: ["text"],
                    instructions: "Please assist the user.",
                }
            }));
        });
        ws.on("error", (err) => {
            console.error("WebSocket error:", err);
            reject(err); // 发生错误，拒绝 Promise
        });
    });
}


// Function to send user message
async function sendUserMessage(text) {
    const ws = await init_socket()
    const myAudio = fs.readFileSync(text);
    const audioBuffer = await decodeAudio(myAudio);

    const channelData = audioBuffer.getChannelData(0);
    const base64AudioData = base64EncodeAudio(channelData);

    const event = {
    type: 'conversation.item.create',
    item: {
        type: 'message',
        role: 'user',
        content: [
        {
            type: 'input_audio',
            audio: base64AudioData
        }
        ]
    }
    };
    ws.send(JSON.stringify(event));
    ws.send(JSON.stringify({type: 'response.create',response: {
        modalities: ['text','audio'],
        instructions: "What language is spoken in this audio segment?Please choose from the German, English, French, Spanish, and Italian options?",
    }}));

    ws.on("message", async function incoming(message) {
        const obj = JSON.parse(message.toString());
        if ('item' in obj) {
            if (obj.item.content.length != 0) {
                if (obj.item.content[0].type != "input_audio") {
                    console.log("Server response:");
                    console.log(obj.item.content[0]);
                    // 获取输入文件的路径和名称
                    const fileDir = path.dirname(text);  // 获取文件所在目录
                    const baseFileName = path.basename(text, path.extname(text));  // 获取不带扩展名的文件名
                    // 目标输出文件路径
                    const outputFileName = `${baseFileName}_gpt4o_answer.json`;  // 构造输出文件名
                    const outputFilePath = path.join(fileDir, outputFileName);  // 生成输出文件的完整路径
                    await writeFile(outputFilePath, JSON.stringify({
                        voice_relative_path: text,
                        gpt4o_reply: obj.item.content[0],
                    }, null, 2), 'utf8');
                    return obj.item.content[0]
                } else {
                    console.log("Input:");
                    console.log(obj.item.content[0]);
                }
            }

            /*else
            {
                console.log(obj.item.content);
            }*/
        } else {
            //console.log(obj);
        }

    });
}

// 读取 JSON 文件并处理
async function processJsonFile(filePath) {
    console.log("准备路径");

    try {
        // 异步读取 JSON 文件，等待 Promise 解析
        const data = await readFile(filePath, 'utf8');
        console.log("读入成功");

        const dictList = JSON.parse(data);  // 解析 JSON 文件

        if (!Array.isArray(dictList)) {
            console.error("The JSON content is not an array.");
            return;
        }

        const replies = [];  // 存储每个回复的数组

        // 遍历列表中的每个 dict
        for (const item of dictList) {
                // 获取输入文件的路径和名称
            const fileDir = path.dirname(filePath);  // 获取文件所在目录
            const baseFileName = path.basename(filePath, path.extname(filePath));  // 获取不带扩展名的文件名

            // 目标输出文件路径
            const outputFileName = `${baseFileName}_gpt4o_answer.json`;  // 构造输出文件名
            const all_outputFilePath = path.join(fileDir, outputFileName);  // 生成输出文件的完整路径

            if (item.voice_relative_path) {
                // 获取绝对路径
                const absolutePath = path.resolve(item.voice_relative_path);
                // 打印或传递路径到 sendUserMessage 函数
                console.log("Sending:", absolutePath);

                const fileDir = path.dirname(absolutePath);  // 获取文件所在目录
                const baseFileName = path.basename(absolutePath, path.extname(absolutePath));  // 获取不带扩展名的文件名
                // 目标输出文件路径
                const outputFileName = `${baseFileName}_gpt4o_answer.json`;  // 构造输出文件名
                const outputFilePath = path.join(fileDir, outputFileName);  // 生成输出文件的完整路径
                if (!(fs.existsSync(outputFilePath))){
                    try {
                        // 发送消息并等待回复
                        const reply = await sendUserMessage(absolutePath);
                        console.log("reply:", reply);

                        // 将原始的 filepath 和回复一起存储
                        replies.push({
                            voice_relative_path: item.voice_relative_path,
                            gpt4o_reply: reply,
                            question: item.question,
                            answer: item.answer,
                            discript: item.discript,
                        });

                        // 将回复保存到新的 JSON 文件

                        console.log(`Replies successfully saved to ${outputFilePath}`);
                        console.log("Received reply:", reply);
                    } catch (error) {
                        console.error("Error sending message:", error);
                    }
                }
                else {
                    console.log("Jump:", absolutePath)
                }


            } else {
                console.warn("No 'voice_relative_path' attribute in item:", item);
            // 将回复保存到新的 JSON 文件
            await writeFile(all_outputFilePath, JSON.stringify(replies, null, 2), 'utf8');
            console.log(`Replies successfully saved to ${all_outputFilePath}`);
            }
        }
    } catch (error) {
        console.error("Error reading or processing the JSON file:", error);
    }
}

// 调用函数处理 JSON 文件（假设文件名为 'aaa.bb'）
processJsonFile('C:\\Users\\23225\\PycharmProjects\\SpeechDataPreprocess\\gpt4O_all\\Language Identification\\Q_What_language_is_filter.json');
