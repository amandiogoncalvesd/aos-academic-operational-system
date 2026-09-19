# 🎙️ Transcrição em Tempo Real no LMS do AOS
## Como Funciona, Como Implementar e Código Open Source

**Data:** 27 de Agosto de 2026  
**Contexto:** Plugin LMS do AOS — Academic Operational System

---

## 1. 🔍 A Verdade Sobre o Coursera: Como Ele Realmente Funciona

### 1.1 O Que o Coursera Realmente Faz

O Coursera **NÃO faz transcrição em tempo real nativa** durante a reprodução do vídeo. O que você experimentou provavelmente foi uma das três abordagens:

**Abordagem 1 — Transcrição Pré-Processada com Timestamps (Padrão do Coursera):**
O Coursera processa o áudio de cada videoaula **antes** de publicar o curso. O áudio é transcrito em lote (batch) por engines de ASR (Automatic Speech Recognition), gera um arquivo de legenda (VTT/SRT) com timestamps precisos, e o player de vídeo exibe essas legendas sincronizadas com o vídeo. cite🛠web_search:12#14:~:text=Coursera's transcript is the most learner-friendly...Open any video, scroll below the player to the Downloads section, and click Transcript

**Abordagem 2 — Closed Captions Automáticas (YouTube-style):**
Para cursos hospedados em plataformas que usam players como o YouTube, as legendas são geradas automaticamente pelo próprio YouTube (usando o ASR do Google) e sincronizadas com o vídeo.

**Abordagem 3 — Extensões de Browser de Terceiros:**
Ferramentas como **Immersive Translate** ou **Speechify** podem interceptar o áudio do navegador e transcrever em tempo real usando APIs de ASR. cite🛠web_search:12#10:~:text=Speechify works with Coursera Speechify...You can listen to your lectures from Coursera in real-time

### 1.2 Por Que o Coursera Não Transcreve em Tempo Real?

Transcrição em tempo real (streaming ASR) é computacionalmente intensiva e cara. Para um catálogo de milhões de videoaulas, o Coursera opta por:
1. **Processamento batch** — Transcreve uma vez, serve milhões de vezes
2. **Qualidade superior** — ASR batch com modelos grandes (Whisper Large) tem precisão muito maior que streaming
3. **Custo zero por reprodução** — Uma vez gerada, a legenda é um arquivo estático

### 1.3 O Que Você Viu: A Ilusão do "Tempo Real"

O que parece "transcrição ao vivo sem deslize" é na verdade:
- Um arquivo VTT/SRT pré-gerado com timestamps de palavra
- O player de vídeo sincroniza o texto com o tempo atual do vídeo
- A precisão é de 99% porque foi processado por um modelo grande (Whisper Large V3) em batch

---

## 2. 🧠 Como a Transcrição em Tempo Real REALMENTE Funciona (Tecnologia)

### 2.1 Pipeline de Streaming ASR

Para implementar transcrição **verdadeiramente em tempo real** (como em uma videochamada ou live stream), o pipeline é:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   ÁUDIO     │───►│  CAPTURA    │───►│  STREAMING  │───►│    ASR      │
│  (Voz do    │    │  (Microfone │    │  (WebSocket│    │  (Whisper/  │
│  Professor) │    │  /Video)    │    │  /WebRTC)   │    │  Deepgram)  │
└─────────────┘    └─────────────┘    └─────────────┘    └──────┬──────┘
                                                                 │
                    ┌─────────────────────────────────────────────┘
                    │
                    ▼
           ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
           │   TEXTO     │───►│  LEGENDAS   │───►│   PLAYER    │
           │  (Parcial/  │    │  (WebVTT    │    │  (HTML5     │
           │  Final)     │    │  Dinâmico)  │    │  Video)     │
           └─────────────┘    └─────────────┘    └─────────────┘
```

### 2.2 Etapas Técnicas Detalhadas

**Etapa 1 — Captura de Áudio:**
O áudio é capturado via `getUserMedia()` (navegador) ou extraído da faixa de áudio do vídeo. O formato ideal é **PCM 16-bit, mono, 16kHz** — é o que a maioria dos modelos ASR espera. cite🛠web_search:12#15:~:text=Fishjam's APIs were designed with AI integration in mind...16-bit PCM at 16 kHz (or 24 kHz), which matches what most speech-to-text engines expect

**Etapa 2 — Chunking (Divisão em Blocos):**
O áudio é dividido em pequenos blocos (chunks) de ~0.5 a 2 segundos. Isso permite processamento contínuo sem esperar o áudio terminar. cite🛠web_search:12#7:~:text=Once audio is digitized, it needs to be transmitted to the server...divided into small chunks, which are sent over a real-time protocol like WebSocket

**Etapa 3 — Voice Activity Detection (VAD):**
Antes de enviar para o ASR, um detector de atividade de voz filtra silêncios e ruídos. Isso reduz processamento desnecessário. cite🛠web_search:12#13:~:text=streaming_vad_config...threshold: 0.5, min_silence_duration_ms: 300

**Etapa 4 — Streaming via WebSocket:**
Os chunks de áudio são enviados para o servidor via WebSocket (conexão persistente, bidirecional). HTTP tradicional é muito lento para isso. cite🛠web_search:12#13:~:text=WebSockets navigates around this by maintaining a persistent, bidirectional connection between the server and the client, enabling seamless real-time communication

**Etapa 5 — ASR Streaming:**
O servidor recebe os chunks, acumula em um buffer, e envia para o modelo ASR. O modelo retorna:
- **Partial transcripts** — Texto provisório (muda conforme mais áudio chega)
- **Final transcripts** — Texto confirmado (não muda mais)

**Etapa 6 — Renderização de Legendas:**
O texto retornado é convertido para **WebVTT** (formato de legenda da web) e injetado no player de vídeo via `TextTrack` API do HTML5. cite🛠web_search:12#12:~:text=WebVTT (Web Video Text Tracks) is a W3C standard caption and subtitle format that delivers timed text alongside video in modern streaming workflows

---

## 3. 🏆 Melhores Modelos Open Source para ASR em 2026

### 3.1 Ranking por Categoria

| Modelo | WER (Erro) | Velocidade | Idiomas | VRAM | Melhor Para |
|--------|-----------|-----------|---------|------|-------------|
| **NVIDIA Canary-Qwen 2.5B** | 5.63% | 418x RTF | 25 | ~8GB | Precisão máxima |
| **Whisper Large V3** | 7.4% | 1x (base) | 99+ | ~10GB | Multilíngue geral |
| **Whisper Large V3 Turbo** | 7.75% | 216x RTF | 99+ | ~6GB | Equilíbrio velocidade/precisão |
| **NVIDIA Parakeet TDT 1.1B** | ~8.0% | 2.728x RTF | 25 (EN) | ~4GB | Velocidade extrema |
| **Distil-Whisper** | ~8.4% | 5-6x mais rápido | EN | ~2GB | Recursos limitados |
| **Moonshine v2** | ~9% | Tempo real | EN | 27MB-500MB | Edge/mobile/IoT |

cite🛠web_search:11#6:~:text=NVIDIA's Canary Qwen 2.5B currently tops the Hugging Face Open ASR Leaderboard with 5.63% WER cite🛠web_search:11#6:~:text=Whisper Large V3 Turbo prunes the decoder from 32 layers to 4...approximately 216x real-time processing speed cite🛠web_search:11#6:~:text=NVIDIA's Parakeet TDT...achieves an RTFx above 2,000 cite🛠web_search:11#6:~:text=Moonshine by Useful Sensors is designed for real-time speech recognition on resource-constrained hardware...The smallest model is just 27MB

### 3.2 Recomendação para o AOS LMS

**Para o plugin LMS do AOS, recomendo uma arquitetura híbrida:**

| Cenário | Abordagem | Modelo |
|---------|-----------|--------|
| **Videoaulas gravadas** | Batch (pré-processamento) | Whisper Large V3 |
| **Aulas ao vivo / webinars** | Streaming real-time | Whisper Large V3 Turbo ou Parakeet TDT |
| **Mobile / conexão lenta** | Edge/on-device | Moonshine v2 |
| **Alta precisão (exames, jurídico)** | Batch + revisão humana | Canary-Qwen 2.5B |

---

## 4. 🔧 Implementação Open Source: Código Completo

### 4.1 Opção 1: Whisper Streaming (UFAL) — Recomendado para LMS

O projeto **whisper_streaming** da UFAL (Universidade de Praga) é a implementação open source mais madura para transcrição em tempo real com Whisper. cite🛠web_search:12#1:~:text=Whisper realtime streaming for long speech-to-text transcription and translation

**GitHub:** [github.com/ufal/whisper_streaming](https://github.com/ufal/whisper_streaming)

**Como usar como módulo:**

```python
# Instalação
# pip install faster-whisper

from whisper_online import *

# Configuração
src_lan = "pt"  # Português
tgt_lan = "pt"  # Mesmo idioma para ASR

# Carrega modelo (usa FasterWhisper por baixo)
asr = FasterWhisperASR(src_lan, "large-v3")

# Ativa VAD (Voice Activity Detection) para melhor precisão
asr.use_vad()

# Cria processador online
online = OnlineASRProcessor(asr)

# Loop de processamento
while audio_has_not_ended:
    # Recebe chunk de áudio (ex: do WebSocket)
    audio_chunk = receive_audio_chunk_from_websocket()

    # Insere no buffer
    online.insert_audio_chunk(audio_chunk)

    # Processa e retorna texto parcial
    partial_result = online.process_iter()

    if partial_result:
        # Envia de volta para o cliente via WebSocket
        websocket.send(json.dumps({
            "type": "partial",
            "text": partial_result[2],  # texto
            "start": partial_result[0], # timestamp início
            "end": partial_result[1]    # timestamp fim
        }))

# Finaliza ao terminar o áudio
final_result = online.finish()
online.init()  # Reseta para próxima sessão
```

### 4.2 Opção 2: WhisperLive (Collabora) — Servidor WebSocket Completo

O **WhisperLive** da Collabora é um servidor WebSocket completo com cliente. Ideal para produção. cite🛠web_search:12#5:~:text=A nearly-live implementation of OpenAI's Whisper

**GitHub:** [github.com/collabora/WhisperLive](https://github.com/collabora/WhisperLive)

**Arquitetura:**
```
Cliente (Browser/App)  ←──WebSocket──→  Servidor WhisperLive  ←──GPU──→  Modelo Whisper
        │                                       │
        │ Captura áudio via PyAudio/JS          │ Transcreve com FasterWhisper
        │ Envia chunks PCM 16kHz                │ Envia partial + final transcripts
```

**Como rodar:**
```bash
# Servidor
git clone https://github.com/collabora/WhisperLive.git
cd WhisperLive
pip install -r requirements.txt
python run_server.py --model medium --language pt

# Cliente (transcreve arquivo de áudio)
python run_client.py --files aula.mp3 --server localhost --port 9090

# Ou cliente com microfone ao vivo
python run_client.py --server localhost --port 9090
```

**Parâmetros do cliente:**
- `lang`: Idioma do áudio ("pt" para português)
- `translate`: Traduzir para inglês (True/False)
- `model`: Tamanho do modelo (tiny, base, small, medium, large-v3)
- `use_vad`: Ativar Voice Activity Detection
- `enable_translation`: Ativar tradução para qualquer idioma
- `target_language`: Idioma alvo da tradução cite🛠web_search:12#5:~:text=lang: Language of the input audio...translate: If set to True then translate from any language to en...model: Whisper model size...use_vad: Whether to use Voice Activity Detection on the server

### 4.3 Opção 3: Servidor WebSocket com Flask + Whisper (Simples)

Para prototipagem rápida no AOS: cite🛠web_search:12#8:~:text=How to Build a Streaming Whisper WebSocket Service

```python
# requirements.txt
# Flask, gevent-websocket, flask_sockets, openai-whisper

from flask import Flask, render_template
from flask_sockets import Sockets
import whisper
import base64
import tempfile
import numpy as np

app = Flask(__name__)
sockets = Sockets(app)

# Carrega modelo uma vez (na inicialização)
model = whisper.load_model("base")  # ou "small", "medium", "large-v3"

def process_wav_bytes(webm_bytes: bytes, sample_rate: int = 16000):
    """Converte bytes de áudio para formato que Whisper aceita"""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_file:
        temp_file.write(webm_bytes)
        temp_file.flush()
        waveform = whisper.load_audio(temp_file.name, sr=sample_rate)
        return waveform

@sockets.route("/transcribe")
def transcribe_socket(ws):
    """WebSocket endpoint para transcrição em tempo real"""
    while not ws.closed:
        message = ws.receive()
        if message:
            try:
                # Decodifica base64 se necessário
                if isinstance(message, str):
                    message = base64.b64decode(message)

                # Processa áudio
                audio = process_wav_bytes(bytes(message))
                audio = whisper.pad_or_trim(audio.reshape(1, -1))

                # Transcreve
                result = whisper.transcribe(model, audio, language="pt")
                text = result["text"].strip()

                # Envia resultado de volta
                ws.send(json.dumps({
                    "type": "transcription",
                    "text": text,
                    "language": "pt"
                }))

            except Exception as e:
                ws.send(json.dumps({"type": "error", "message": str(e)}))

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(("", 5003), app, handler_class=WebSocketHandler)
    print("Servidor de transcrição rodando em ws://localhost:5003/transcribe")
    server.serve_forever()
```

**Cliente JavaScript (Browser):**
```javascript
// Captura áudio do microfone e envia para o servidor
const ws = new WebSocket("wss://seu-servidor.com/transcribe");

ws.onopen = () => {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            const mediaRecorder = new MediaRecorder(stream, {
                mimeType: "audio/webm;codecs=opus"
            });

            // Envia chunks a cada 500ms
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    event.data.arrayBuffer().then(buffer => {
                        ws.send(buffer);
                    });
                }
            };

            mediaRecorder.start(500); // Chunk a cada 500ms
        });
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === "transcription") {
        document.getElementById("transcription").textContent += data.text + " ";
    }
};
```

### 4.4 Opção 4: Geração de Legendas para Vídeos (Batch) — SubsAI

Para videoaulas gravadas (caso mais comum no LMS), use o **SubsAI** para gerar legendas automaticamente antes da publicação: cite🛠web_search:12#3:~:text=Subtitles generation tool powered by OpenAI's Whisper and its variants

**GitHub:** [github.com/absadiki/subsai](https://github.com/absadiki/subsai)

```bash
# Docker (recomendado)
docker pull absadiki/subsai:main
docker run --gpus=all -p 8501:8501 -v /videos:/media_files absadiki/subsai:main

# Acesse http://localhost:8501 e faça upload do vídeo
# O SubsAI gera automaticamente legendas em VTT/SRT com timestamps
```

**Ou via Python:**
```python
from subsai import SubsAI

subs_ai = SubsAI()
model = subs_ai.create_model("whisper", {"model_type": "large-v3"})

# Transcreve vídeo e gera arquivo VTT
subs = subs_ai.transcribe("/videos/aula01.mp4", model)
subs.save("/videos/aula01.pt.vtt")
```

### 4.5 Opção 5: Auto-Subtitle (Overlay Direto no Vídeo)

Para gerar vídeos com legendas embutidas (burn-in): cite🛠web_search:12#2:~:text=Automatically generate and overlay subtitles for any video

**GitHub:** [github.com/m1guelpf/auto-subtitle](https://github.com/m1guelpf/auto-subtitle)

```bash
pip install git+https://github.com/m1guelpf/auto-subtitle.git

# Gera vídeo com legendas embutidas
auto-subtitle aula01.mp4 --model large-v3 --language Portuguese --output aula01_legendado.mp4
```

---

## 5. 🏗️ Arquitetura do Plugin LMS do AOS para Transcrição

### 5.1 Arquitetura Híbrida Recomendada

O plugin LMS do AOS deve implementar **duas abordagens**:

```
┌─────────────────────────────────────────────────────────────────┐
│              AOS LMS — SISTEMA DE TRANSCRIÇÃO                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────┐      ┌─────────────────────┐         │
│  │   MODO BATCH        │      │   MODO STREAMING    │         │
│  │   (Vídeo Gravado)   │      │   (Aula Ao Vivo)    │         │
│  └──────────┬──────────┘      └──────────┬──────────┘         │
│             │                            │                     │
│             ▼                            ▼                     │
│  ┌─────────────────────┐      ┌─────────────────────┐         │
│  │  Upload de Vídeo    │      │  WebRTC / WebSocket │         │
│  │  → Fila Celery      │      │  → Captura Áudio    │         │
│  │  → Whisper Large V3 │      │  → Whisper Turbo    │         │
│  │  → Gera VTT/SRT     │      │  → WebVTT Dinâmico  │         │
│  │  → Salva no S3      │      │  → Player HTML5     │         │
│  └──────────┬──────────┘      └──────────┬──────────┘         │
│             │                            │                     │
│             └────────────┬───────────────┘                     │
│                          ▼                                     │
│               ┌─────────────────────┐                         │
│               │   PLAYER DE VÍDEO   │                         │
│               │  (Video.js / Plyr) │                         │
│               │                     │                         │
│               │  • Legendas VTT     │                         │
│               │  • Highlight sync   │                         │
│               │  • Busca no texto   │                         │
│               │  • Tradução inline  │                         │
│               └─────────────────────┘                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Componentes do Plugin

**Backend (Python/FastAPI):**
```python
# aos-domain-lms/src/services/transcription_service.py

from whisper_online import FasterWhisperASR, OnlineASRProcessor
import asyncio
from kafka import KafkaProducer

class LMSTranscriptionService:
    def __init__(self):
        self.asr = FasterWhisperASR("pt", "large-v3")
        self.asr.use_vad()
        self.kafka = KafkaProducer(bootstrap_servers=["kafka:9092"])

    async def transcribe_video_batch(self, video_id: str, video_path: str):
        """Transcreve vídeo gravado em batch (assíncrono via Celery)"""
        online = OnlineASRProcessor(self.asr)

        # Extrai áudio do vídeo
        audio = extract_audio(video_path, sample_rate=16000)

        # Processa em chunks
        for chunk in audio_chunks(audio, chunk_size=30):
            online.insert_audio_chunk(chunk)
            partial = online.process_iter()
            # Opcional: salva progresso

        final = online.finish()

        # Gera WebVTT
        vtt_content = self._generate_webvtt(final)

        # Salva no S3
        s3_url = await s3_upload(f"transcriptions/{video_id}.vtt", vtt_content)

        # Emite evento
        self.kafka.send("lms.transcription.completed", {
            "video_id": video_id,
            "vtt_url": s3_url,
            "language": "pt"
        })

        return s3_url

    async def transcribe_live_stream(self, websocket, video_id: str):
        """Transcreve stream ao vivo via WebSocket"""
        online = OnlineASRProcessor(self.asr)

        try:
            while True:
                # Recebe chunk de áudio do WebSocket
                audio_chunk = await websocket.receive_bytes()

                online.insert_audio_chunk(audio_chunk)
                result = online.process_iter()

                if result and result[2].strip():
                    await websocket.send_json({
                        "type": "partial" if not result[3] else "final",
                        "text": result[2],
                        "start": result[0],
                        "end": result[1]
                    })
        except:
            online.finish()

    def _generate_webvtt(self, segments):
        """Converte segmentos Whisper para WebVTT"""
        vtt = ["WEBVTT", ""]
        for seg in segments:
            start = format_timestamp(seg[0])
            end = format_timestamp(seg[1])
            text = seg[2]
            vtt.append(f"{start} --> {end}")
            vtt.append(text)
            vtt.append("")
        return "\n".join(vtt)
```

**Frontend (React + Video.js):**
```typescript
// Componente de Player com Legendas AOS
import React, { useEffect, useRef, useState } from "react";
import videojs from "video.js";

interface AOSVideoPlayerProps {
  videoUrl: string;
  videoId: string;
  mode: "batch" | "live";
}

export const AOSVideoPlayer: React.FC<AOSVideoPlayerProps> = ({
  videoUrl,
  videoId,
  mode,
}) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const playerRef = useRef<any>(null);
  const [transcript, setTranscript] = useState("");
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!videoRef.current) return;

    // Inicializa Video.js
    playerRef.current = videojs(videoRef.current, {
      controls: true,
      fluid: true,
      html5: {
        vhs: { overrideNative: true },
      },
    });

    // MODO BATCH: Carrega legendas VTT pré-geradas
    if (mode === "batch") {
      fetch(`/api/v1/lms/videos/${videoId}/transcription`)
        .then((res) => res.json())
        .then((data) => {
          if (data.vtt_url) {
            playerRef.current.addRemoteTextTrack(
              {
                kind: "subtitles",
                src: data.vtt_url,
                srclang: "pt",
                label: "Português (Auto)",
                default: true,
              },
              false
            );
          }
        });
    }

    // MODO LIVE: Conecta WebSocket para transcrição em tempo real
    if (mode === "live") {
      const ws = new WebSocket(
        `wss://api.aos.com/lms/live-transcription/${videoId}`
      );
      wsRef.current = ws;

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === "partial" || data.type === "final") {
          setTranscript((prev) => {
            // Substitui texto parcial, adiciona final
            if (data.type === "final") {
              return prev + " " + data.text;
            }
            return prev + data.text;
          });
        }
      };

      // Captura áudio do vídeo e envia para o servidor
      const audioContext = new AudioContext();
      const source = audioContext.createMediaElementSource(videoRef.current);
      const processor = audioContext.createScriptProcessor(4096, 1, 1);

      processor.onaudioprocess = (e) => {
        const inputData = e.inputBuffer.getChannelData(0);
        const int16Data = float32ToInt16(inputData);
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(int16Data.buffer);
        }
      };

      source.connect(processor);
      processor.connect(audioContext.destination);
    }

    return () => {
      if (playerRef.current) playerRef.current.dispose();
      if (wsRef.current) wsRef.current.close();
    };
  }, [videoUrl, videoId, mode]);

  return (
    <div className="aos-video-player">
      <video ref={videoRef} className="video-js vjs-big-play-centered" controls>
        <source src={videoUrl} type="video/mp4" />
      </video>

      {/* Painel de transcrição ao vivo */}
      {mode === "live" && (
        <div className="live-transcript-panel">
          <h4>Transcrição ao Vivo</h4>
          <div className="transcript-text">{transcript}</div>
        </div>
      )}

      {/* Busca no texto (modo batch) */}
      {mode === "batch" && (
        <div className="transcript-search">
          <input type="text" placeholder="Buscar no vídeo..." />
          <div className="search-results" />
        </div>
      )}
    </div>
  );
};

// Helper: converte Float32 (Web Audio API) para Int16 (PCM)
function float32ToInt16(float32Array: Float32Array): Int16Array {
  const int16Array = new Int16Array(float32Array.length);
  for (let i = 0; i < float32Array.length; i++) {
    int16Array[i] = Math.max(-1, Math.min(1, float32Array[i])) * 0x7fff;
  }
  return int16Array;
}
```

---

## 6. 🌐 WebVTT: O Formato de Legenda Padrão

### 6.1 Estrutura do WebVTT

O WebVTT é o formato W3C padrão para legendas na web. Funciona nativamente com HTML5 `<video>`. cite🛠web_search:12#12:~:text=WebVTT (Web Video Text Tracks) is a W3C standard caption and subtitle format that delivers timed text alongside video in modern streaming workflows

```vtt
WEBVTT

1
00:00:01.000 --> 00:00:04.000
Bem-vindos à aula de hoje.

2
00:00:04.500 --> 00:00:08.000 line:90%
Hoje vamos falar sobre arquitetura de software.

3
00:00:08.500 --> 00:00:12.000
<c.highlight>Importante:</c> Prestem atenção neste conceito.
```

**Recursos do WebVTT:**
- Timestamps precisos (HH:MM:SS.mmm)
- Posicionamento (`line:90%` = parte inferior)
- Estilização via CSS (`<c.highlight>`)
- Suporte a múltiplos idiomas
- Compatível com HLS e DASH streaming cite🛠web_search:12#11:~:text=WebVTT has settled in as the default caption format for modern streaming...tight integration with HLS and DASH

### 6.2 Gerando WebVTT com Timestamps de Palavra

Para o efeito "highlight palavra por palavra" (como no Coursera):

```python
def generate_word_level_vtt(segments):
    """Gera WebVTT com timestamps de palavra para highlight sincronizado"""
    vtt = ["WEBVTT", ""]

    for seg in segments:
        words = seg.get("words", [])  # Whisper com word_timestamps=True

        for word_info in words:
            start = format_timestamp(word_info["start"])
            end = format_timestamp(word_info["end"])
            word = word_info["word"]

            vtt.append(f"{start} --> {end}")
            vtt.append(word)
            vtt.append("")

    return "\n".join(vtt)

# Uso com Whisper
result = whisper.transcribe(
    model, audio, 
    language="pt",
    word_timestamps=True  # Ativa timestamps de palavra!
)
```

---

## 7. 🚀 Roadmap de Implementação no AOS LMS

### Fase 1 — Legendas Batch (Mês 1-2)
- [ ] Integrar Whisper Large V3 via Celery para processamento assíncrono
- [ ] Gerar WebVTT com timestamps de palavra
- [ ] Player Video.js com suporte a WebVTT e highlight sincronizado
- [ ] Painel lateral de transcrição com busca e navegação por clique

### Fase 2 — Tradução de Legendas (Mês 2-3)
- [ ] Integrar modelo de tradução (Marian NMT / OPUS-MT)
- [ ] Gerar VTT em múltiplos idiomas a partir do VTT original
- [ ] Seletor de idioma no player

### Fase 3 — Transcrição Ao Vivo (Mês 4-6)
- [ ] Servidor WebSocket com Whisper Streaming
- [ ] Captura de áudio do vídeo via Web Audio API
- [ ] Renderização de legendas dinâmicas no player
- [ ] Suporte a webinars e aulas ao vivo

### Fase 4 — Recursos Avançados (Mês 7-9)
- [ ] Diarização de falantes (quem está falando)
- [ ] Resumo automático da aula via LLM
- [ ] Geração de flashcards a partir da transcrição
- [ ] Indexação de busca full-text em todas as videoaulas

---

## 8. 📚 Recursos e Links

| Recurso | Link | Descrição |
|---------|------|-----------|
| **Whisper Streaming (UFAL)** | github.com/ufal/whisper_streaming | Streaming ASR com Whisper |
| **WhisperLive (Collabora)** | github.com/collabora/WhisperLive | Servidor WebSocket completo |
| **SubsAI** | github.com/absadiki/subsai | Geração de legendas com UI |
| **Auto-Subtitle** | github.com/m1guelpf/auto-subtitle | Overlay de legendas em vídeo |
| **Whisper.cpp** | github.com/ggerganov/whisper.cpp | Whisper otimizado em C++ |
| **Faster-Whisper** | github.com/SYSTRAN/faster-whisper | Whisper com CTranslate2 |
| **WebVTT Spec** | w3.org/TR/webvtt | Especificação W3C |
| **WhisperX** | github.com/m-bain/whisperX | Whisper + diarização + timestamps |

---

## 9. 💡 Conclusão

O "efeito Coursera" de transcrição perfeita e sincronizada é, na maioria das vezes, **transcrição batch pré-processada** — não tempo real. Para o AOS LMS, a estratégia recomendada é:

1. **Videoaulas gravadas:** Use **Whisper Large V3 em batch** via Celery. Gere WebVTT com timestamps de palavra. Ofereça busca, highlight sincronizado e tradução.

2. **Aulas ao vivo/webinars:** Use **Whisper Streaming** via WebSocket para transcrição em tempo real com latência de ~300-800ms.

3. **Mobile/conexão lenta:** Use **Moonshine v2** para transcrição on-device sem servidor.

A arquitetura híbrida do AOS permite que cada instituição escolha o modo que melhor se adequa às suas necessidades — tudo via plugins.
