# 🎙️ AOS LMS — Speech-to-Speech Translation (S2ST)
## Dublagem Automática via IA: Áudio em Português → Áudio em Qualquer Idioma

**Versão:** 1.0  
**Data:** 27 de Agosto de 2026  
**Contexto:** Plugin LMS do AOS — Tradução de videoaulas para múltiplos idiomas

---

## 📋 Sumário Executivo

O que você descreveu é **Speech-to-Speech Translation (S2ST)** — a tradução direta de áudio falado em um idioma para áudio falado em outro idioma, preservando a voz, o tom e o ritmo do orador original. Isso é radicalmente diferente de legendas: o aluno **ouve** a aula no idioma dele, não lê.

O AOS LMS implementará um pipeline de **dublagem automática via IA** que:
1. Extrai o áudio do vídeo da aula
2. Transcreve com timestamps de palavra (ASR)
3. Identifica quem fala (diarização)
4. Traduz o texto para N idiomas
5. Clona a voz do professor e sintetiza áudio traduzido (TTS)
6. Sincroniza o áudio novo com o vídeo original
7. Gera um arquivo de vídeo com **múltiplas faixas de áudio** (como um DVD)
8. O aluno escolhe o idioma de áudio no player

---

## 1. 🧬 O Que é Speech-to-Speech Translation (S2ST)

### 1.1 Diferença Fundamental

| Característica | Legendas (Subtitles) | Dublagem Automática (S2ST) |
|----------------|---------------------|---------------------------|
| **Saída** | Texto na tela | Áudio falado |
| **Experiência** | Aluno lê enquanto assiste | Aluno ouve naturalmente |
| **Carga cognitiva** | Alta (dividir atenção) | Baixa (foco no vídeo) |
| **Acessibilidade** | Limitada (analfabetos, cegos) | Universal |
| **Tecnologia** | ASR + WebVTT | ASR + NMT + TTS + Sync |
| **Complexidade** | Média | Alta |

### 1.2 Pipeline S2ST Completo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PIPELINE S2ST — DUBLAGEM AUTOMÁTICA AOS                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐           │
│  │  VÍDEO   │───►│  EXTRAIR │───►│    ASR   │───►│ DIARIZA- │           │
│  │  AULA    │    │   ÁUDIO  │    │ (Whisper)│    │   ÇÃO    │           │
│  │  .mp4    │    │  FFmpeg  │    │          │    │(pyannote)│           │
│  └──────────┘    └──────────┘    └────┬─────┘    └────┬─────┘           │
│                                        │               │                  │
│                                        ▼               ▼                  │
│                              ┌─────────────────────────────┐             │
│                              │  TEXTO + TIMESTAMPS + FALANTE│             │
│                              │  "00:01.200 → 00:03.500"     │             │
│                              │  "Prof. Silva: Bem-vindos..."│             │
│                              └──────────────┬──────────────┘             │
│                                             │                             │
│                              ┌──────────────┼──────────────┐             │
│                              │              │              │             │
│                              ▼              ▼              ▼             │
│                        ┌─────────┐   ┌─────────┐   ┌─────────┐        │
│                        │TRADUÇÃO │   │TRADUÇÃO │   │TRADUÇÃO │        │
│                        │  EN     │   │  ES     │   │  FR     │        │
│                        │(NLLB/  │   │(NLLB/  │   │(NLLB/  │        │
│                        │ M2M100)│   │ M2M100)│   │ M2M100)│        │
│                        └────┬────┘   └────┬────┘   └────┬────┘        │
│                             │              │              │             │
│                             ▼              ▼              ▼             │
│                        ┌─────────┐   ┌─────────┐   ┌─────────┐        │
│                        │  TTS    │   │  TTS    │   │  TTS    │        │
│                        │(XTTS v2 │   │(XTTS v2 │   │(XTTS v2 │        │
│                        │Voice    │   │Voice    │   │Voice    │        │
│                        │Clone)   │   │Clone)   │   │Clone)   │        │
│                        └────┬────┘   └────┬────┘   └────┬────┘        │
│                             │              │              │             │
│                             ▼              ▼              ▼             │
│                        ┌─────────┐   ┌─────────┐   ┌─────────┐        │
│                        │audio_en.│   │audio_es.│   │audio_fr.│        │
│                        │   wav   │   │   wav   │   │   wav   │        │
│                        └────┬────┘   └────┬────┘   └────┬────┘        │
│                             │              │              │             │
│                             └──────────────┼──────────────┘             │
│                                            │                              │
│                                            ▼                              │
│                              ┌─────────────────────────────┐             │
│                              │  MUX COM VÍDEO (FFmpeg)     │             │
│                              │  Vídeo original +           │             │
│                              │  Faixa PT (original) +        │             │
│                              │  Faixa EN + Faixa ES + ...  │             │
│                              │  → arquivo .mp4 multi-audio │             │
│                              └──────────────┬──────────────┘             │
│                                             │                             │
│                                             ▼                             │
│                              ┌─────────────────────────────┐             │
│                              │  OU: HLS COM FAIXAS ALT.    │             │
│                              │  master.m3u8 com              │             │
│                              │  #EXT-X-MEDIA para cada idioma│             │
│                              └──────────────┬──────────────┘             │
│                                             │                             │
│                                             ▼                             │
│                              ┌─────────────────────────────┐             │
│                              │  PLAYER AOS (Video.js/hls.js)│             │
│                              │  Aluno clica no ícone 🌐     │             │
│                              │  e escolhe: Português,        │             │
│                              │  English, Español, Français...│             │
│                              └─────────────────────────────┘             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. 🏗️ Arquitetura do Plugin `aos-domain-lms-s2st`

### 2.1 Estrutura do Plugin

```
aos-domain-lms-s2st/
├── manifest.json
├── config/
│   └── settings.yaml
├── src/
│   ├── models/
│   │   ├── dubbing_job.py       # Job de dublagem (status, progresso)
│   │   ├── audio_track.py       # Faixa de áudio (idioma, formato, URL)
│   │   └── voice_profile.py     # Perfil de voz clonada do professor
│   ├── services/
│   │   ├── pipeline_service.py  # Orquestra o pipeline S2ST
│   │   ├── asr_service.py       # Whisper ASR com timestamps
│   │   ├── diarization_service.py # pyannote.audio - quem fala
│   │   ├── translation_service.py # NLLB/M2M100/LLM
│   │   ├── tts_service.py         # XTTS v2 / CosyVoice / Edge-TTS
│   │   ├── sync_service.py        # Alinhamento temporal áudio/vídeo
│   │   ├── mux_service.py         # FFmpeg mux multi-audio
│   │   └── hls_service.py         # Geração HLS com faixas alternativas
│   ├── controllers/
│   │   └── dubbing_controller.py
│   ├── workers/
│   │   └── dubbing_worker.py    # Celery worker para processamento batch
│   └── migrations/
├── frontend/
│   └── components/
│       └── LanguageSelector.tsx  # Seletor de idioma no player
└── tests/
```

### 2.2 Manifest do Plugin

```json
{
  "id": "aos-domain-lms-s2st",
  "name": "AOS LMS Speech-to-Speech Translation",
  "version": "1.0.0",
  "type": "domain",
  "dependencies": {
    "aos-core-eventbus": "^2.0.0",
    "aos-domain-lms": "^3.0.0"
  },
  "hooks": {
    "actions": [
      "lms.video.uploaded",
      "lms.dubbing.completed",
      "lms.dubbing.failed"
    ],
    "filters": [
      "lms.video.player.config"
    ]
  },
  "supported_languages": [
    "pt", "en", "es", "fr", "de", "it", "zh", "ja", "ar", "ru"
  ]
}
```

---

## 3. 🔬 Tecnologias Open Source por Etapa

### 3.1 Etapa 1: ASR — Automatic Speech Recognition

**WhisperX** (recomendado) — Whisper com diarização e timestamps de palavra integrados.

```python
import whisperx
import torch

def transcribe_with_diarization(audio_path: str, device: str = "cuda"):
    """Transcreve áudio com timestamps de palavra e identificação de falantes"""

    # 1. Carrega modelo Whisper
    model = whisperx.load_model("large-v3", device, compute_type="float16")

    # 2. Transcreve
    audio = whisperx.load_audio(audio_path)
    result = model.transcribe(audio, batch_size=16, language="pt")

    # 3. Alinha timestamps de palavra
    model_a, metadata = whisperx.load_align_model(language_code="pt", device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device)

    # 4. Diarização (quem fala)
    diarize_model = whisperx.DiarizationPipeline(use_auth_token=HF_TOKEN, device=device)
    diarize_segments = diarize_model(audio)

    # 5. Atribui falantes aos segmentos
    result = whisperx.assign_word_speakers(diarize_segments, result)

    return result

# Saída:
# {
#   "segments": [
#     {
#       "start": 0.0, "end": 3.5,
#       "text": "Bem-vindos à aula de hoje.",
#       "speaker": "SPEAKER_01",
#       "words": [
#         {"word": "Bem-vindos", "start": 0.0, "end": 0.8},
#         {"word": "à", "start": 0.8, "end": 1.0},
#         ...
#       ]
#     }
#   ]
# }
```

**Por que WhisperX e não Whisper puro?**
- Timestamps de **palavra** (não só de frase) — essencial para sincronização precisa
- **Diarização** integrada — identifica múltiplos falantes (professor, aluno, entrevistado)
- Batch processing para velocidade

### 3.2 Etapa 2: Tradução — Neural Machine Translation

**Opção A: NLLB-200 (Meta)** — Modelo open source que traduz entre 200 idiomas. Ideal para tradução direta. cite🛠web_search:14#12:~:text=Meta is making SeamlessM4T available under a research license...NLLB, a text-to-text model for 200 languages

**Opção B: M2M100 (Meta)** — Modelo multilíngue 100x100, traduz diretamente entre qualquer par de idiomas sem passar pelo inglês. cite🛠web_search:14#13:~:text=The transcribed text is fed into the M2M100 model, translating it into your desired target language

**Opção C: LLM (Ollama/Local)** — Para contexto acadêmico técnico, um LLM local (Llama 3, Qwen) pode traduzir com melhor compreensão de termos técnicos. cite🛠web_search:14#0:~:text=AutoDub now supports fully offline translation using Ollama...ideal for privacy, avoiding API limits

```python
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

def translate_segments(segments: list, target_lang: str = "en"):
    """Traduz segmentos de áudio para o idioma alvo"""

    # Carrega NLLB-200
    model_name = "facebook/nllb-200-distilled-600M"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to("cuda")

    translated = []
    for seg in segments:
        text = seg["text"]

        # Tokeniza com idioma alvo
        inputs = tokenizer(text, return_tensors="pt").to("cuda")
        forced_bos_token_id = tokenizer.lang_code_to_id[target_lang]

        # Traduz
        translated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=forced_bos_token_id,
            max_length=512
        )

        translated_text = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

        translated.append({
            "start": seg["start"],
            "end": seg["end"],
            "speaker": seg["speaker"],
            "original_text": text,
            "translated_text": translated_text,
            "words": seg.get("words", [])
        })

    return translated
```

### 3.3 Etapa 3: TTS — Text-to-Speech com Voice Cloning

**Opção A: Coqui XTTS v2** (Recomendado para clonagem de voz)
- Clona a voz do professor com apenas **6 segundos** de amostra
- Suporta 17 idiomas
- Emoção e entonação preservadas cite🛠web_search:14#0:~:text=XTTS: Voice cloning from 6-10 second samples cite🛠web_search:14#13:~:text=Coqui XTTS clones the original speaker's voice in the target language

**Opção B: CosyVoice 2 (FunAudioLLM)**
- Latência de **150ms** em modo streaming
- Suporta emoções e dialetos
- Ideal para dublagem em tempo real cite🛠web_search:14#9:~:text=CosyVoice 2...streaming speech synthesis model...ultra-low latency of 150ms...fine-grained control over emotions and dialects

**Opção C: Edge-TTS (Microsoft)**
- Gratuito, alta qualidade
- Sem clonagem de voz (usa vozes padrão)
- Ideal como fallback cite🛠web_search:14#0:~:text=Edge TTS: High-quality Microsoft voices (recommended)

**Opção D: IndexTTS-2**
- Controle **preciso de duração** — fundamental para sincronização com vídeo
- Desacoplamento de emoção e identidade do falante cite🛠web_search:14#9:~:text=IndexTTS2...precise duration control specifically for video dubbing...disentangled emotional expression and speaker identity control

```python
from TTS.api import TTS
import torch

def clone_and_synthesize(segments: list, speaker_sample: str, target_lang: str):
    """Clona a voz do professor e sintetiza áudio traduzido"""

    # Carrega XTTS v2
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda")

    synthesized_segments = []

    for seg in segments:
        text = seg["translated_text"]
        output_path = f"segments/{seg['speaker']}_{seg['start']:.3f}.wav"

        # Sintetiza com clonagem de voz
        tts.tts_to_file(
            text=text,
            speaker_wav=speaker_sample,  # 6s de amostra da voz do professor
            language=target_lang,        # "en", "es", "fr", etc.
            file_path=output_path
        )

        synthesized_segments.append({
            **seg,
            "audio_path": output_path
        })

    return synthesized_segments
```

### 3.4 Etapa 4: Sincronização Temporal

O áudio sintetizado precisa ter a **mesma duração** do áudio original para não desincronizar com o vídeo.

```python
from pydub import AudioSegment
import librosa

def synchronize_audio(segments: list, target_duration: float):
    """Ajusta a velocidade do áudio sintetizado para corresponder ao original"""

    for seg in segments:
        audio = AudioSegment.from_wav(seg["audio_path"])
        original_duration = seg["end"] - seg["start"]
        synthesized_duration = len(audio) / 1000.0  # ms → s

        # Calcula fator de velocidade
        speed_factor = synthesized_duration / original_duration

        # Ajusta velocidade com librosa (time stretching)
        y, sr = librosa.load(seg["audio_path"], sr=None)
        y_stretched = librosa.effects.time_stretch(y, rate=speed_factor)

        # Salva áudio sincronizado
        librosa.output.write_wav(seg["audio_path"], y_stretched, sr)

    return segments
```

### 3.5 Etapa 5: Mux com Vídeo — Múltiplas Faixas de Áudio

#### Opção A: Arquivo Único com Múltiplas Faixas (MP4/MKV)

```bash
# FFmpeg: Adicionar múltiplas faixas de áudio a um vídeo
ffmpeg -i video_original.mp4   -i audio_portugues.wav   -i audio_english.wav   -i audio_espanol.wav   -i audio_francais.wav   -map 0:v:0   -map 1:a:0   -map 2:a:0   -map 3:a:0   -map 4:a:0   -metadata:s:a:0 language=por   -metadata:s:a:1 language=eng   -metadata:s:a:2 language=spa   -metadata:s:a:3 language=fra   -metadata:s:a:0 title="Português (Original)"   -metadata:s:a:1 title="English (Dubbed)"   -metadata:s:a:2 title="Español (Doblado)"   -metadata:s:a:3 title="Français (Doublé)"   -disposition:a:0 default   -c:v copy   -c:a aac -b:a 192k   -shortest   video_multilanguage.mp4
```

**Problema:** Nem todos os navegadores suportam seleção de faixas de áudio em MP4 via HTML5. cite🛠web_search:15#7:~:text=The hard part isn't the dropdown, it's the manifest

#### Opção B: HLS com Faixas Alternativas (RECOMENDADO para Web)

HLS (HTTP Live Streaming) é o padrão da indústria para streaming com múltiplas faixas de áudio. Funciona em todos os navegadores modernos. cite🛠web_search:15#7:~:text=We'll add a working language picker to an HLS player. The hard part isn't the dropdown, it's the manifest

**Passo 1: Extrair áudio e vídeo separadamente**
```bash
# Extrair vídeo sem áudio
ffmpeg -i video_original.mp4 -an -c:v copy video_only.mp4

# Extrair áudio original (Português)
ffmpeg -i video_original.mp4 -vn -c:a aac -b:a 128k audio_pt.m4a

# Áudios traduzidos já gerados pelo TTS
# audio_en.m4a, audio_es.m4a, audio_fr.m4a
```

**Passo 2: Segmentar com Shaka Packager**
```bash
packager   in=video_only.mp4,stream=video,init_segment=video/init.mp4,segment_template=video/$Number$.m4s,playlist_name=video/video.m3u8   in=audio_pt.m4a,stream=audio,hls_group_id=audio,hls_name=Portugues,language=pt,init_segment=audio_pt/init.mp4,segment_template=audio_pt/$Number$.m4s,playlist_name=audio/pt.m3u8   in=audio_en.m4a,stream=audio,hls_group_id=audio,hls_name=English,language=en,init_segment=audio_en/init.mp4,segment_template=audio_en/$Number$.m4s,playlist_name=audio/en.m3u8   in=audio_es.m4a,stream=audio,hls_group_id=audio,hls_name=Espanol,language=es,init_segment=audio_es/init.mp4,segment_template=audio_es/$Number$.m4s,playlist_name=audio/es.m3u8   in=audio_fr.m4a,stream=audio,hls_group_id=audio,hls_name=Francais,language=fr,init_segment=audio_fr/init.mp4,segment_template=audio_fr/$Number$.m4s,playlist_name=audio/fr.m3u8   --hls_master_playlist_output master.m3u8   --segment_duration 4
```

**Resultado: `master.m3u8`**
```m3u8
#EXTM3U
#EXT-X-VERSION:6

#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio",NAME="Portugues",LANGUAGE="pt",DEFAULT=YES,AUTOSELECT=YES,URI="audio/pt.m3u8"
#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio",NAME="English",LANGUAGE="en",DEFAULT=NO,AUTOSELECT=YES,URI="audio/en.m3u8"
#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio",NAME="Espanol",LANGUAGE="es",DEFAULT=NO,AUTOSELECT=YES,URI="audio/es.m3u8"
#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio",NAME="Francais",LANGUAGE="fr",DEFAULT=NO,AUTOSELECT=YES,URI="audio/fr.m3u8"

#EXT-X-STREAM-INF:BANDWIDTH=2000000,CODECS="avc1.640028,mp4a.40.2",AUDIO="audio"
video/video.m3u8
```

---

## 4. 🎨 Frontend: Player com Seletor de Idioma de Áudio

### 4.1 Video.js com hls.js

```typescript
// components/AOSVideoPlayerWithDubbing.tsx
import React, { useEffect, useRef, useState } from "react";
import Hls from "hls.js";

interface AudioTrack {
  id: number;
  name: string;
  lang: string;
  default: boolean;
}

interface AOSVideoPlayerProps {
  hlsUrl: string; // URL do master.m3u8
  poster?: string;
}

export const AOSVideoPlayerWithDubbing: React.FC<AOSVideoPlayerProps> = ({
  hlsUrl,
  poster,
}) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [audioTracks, setAudioTracks] = useState<AudioTrack[]>([]);
  const [currentTrack, setCurrentTrack] = useState<number>(0);
  const [hlsInstance, setHlsInstance] = useState<Hls | null>(null);

  useEffect(() => {
    if (!videoRef.current) return;

    const video = videoRef.current;

    if (Hls.isSupported()) {
      const hls = new Hls({
        maxBufferLength: 30,
        maxMaxBufferLength: 600,
      });

      hls.loadSource(hlsUrl);
      hls.attachMedia(video);

      // Quando as faixas de áudio são carregadas
      hls.on(Hls.Events.AUDIO_TRACKS_UPDATED, (_evt, data) => {
        const tracks = data.audioTracks.map((track, index) => ({
          id: index,
          name: track.name || track.lang,
          lang: track.lang,
          default: track.default || false,
        }));
        setAudioTracks(tracks);

        // Define a faixa padrão
        const defaultTrack = tracks.find((t) => t.default);
        if (defaultTrack) {
          setCurrentTrack(defaultTrack.id);
        }
      });

      // Detecta mudança de faixa
      hls.on(Hls.Events.AUDIO_TRACK_SWITCHED, (_evt, data) => {
        setCurrentTrack(data.id);
        console.log(`Audio switched to track ${data.id}`);
      });

      setHlsInstance(hls);

      return () => {
        hls.destroy();
      };
    } else if (video.canPlayType("application/vnd.apple.mpegurl")) {
      // Safari nativo
      video.src = hlsUrl;
    }
  }, [hlsUrl]);

  const handleTrackChange = (trackId: number) => {
    if (hlsInstance) {
      hlsInstance.audioTrack = trackId;
    }
  };

  return (
    <div className="aos-dubbed-player">
      <video
        ref={videoRef}
        className="video-js vjs-big-play-centered"
        controls
        poster={poster}
        style={{ width: "100%", height: "auto" }}
      />

      {/* Seletor de idioma de áudio */}
      {audioTracks.length > 1 && (
        <div className="audio-language-selector">
          <span className="selector-label">🌐 Idioma do Áudio:</span>
          <div className="language-buttons">
            {audioTracks.map((track) => (
              <button
                key={track.id}
                className={`lang-btn ${currentTrack === track.id ? "active" : ""}`}
                onClick={() => handleTrackChange(track.id)}
                title={track.name}
              >
                {getLanguageFlag(track.lang)} {track.name}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Legendas (opcional, em paralelo) */}
      <div className="subtitle-toggle">
        <label>
          <input type="checkbox" /> Mostrar legendas traduzidas
        </label>
      </div>
    </div>
  );
};

// Helper: bandeiras por código de idioma
function getLanguageFlag(lang: string): string {
  const flags: Record<string, string> = {
    pt: "🇵🇹", en: "🇬🇧", es: "🇪🇸", fr: "🇫🇷",
    de: "🇩🇪", it: "🇮🇹", zh: "🇨🇳", ja: "🇯🇵",
    ar: "🇸🇦", ru: "🇷🇺", ko: "🇰🇷", hi: "🇮🇳",
  };
  return flags[lang] || "🌐";
}
```

### 4.2 CSS para o Seletor

```css
.audio-language-selector {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: #1a1a2e;
  border-radius: 8px;
  margin-top: 8px;
}

.selector-label {
  color: #e0e0e0;
  font-weight: 600;
  font-size: 14px;
}

.language-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.lang-btn {
  padding: 6px 14px;
  border: 1px solid #333;
  border-radius: 20px;
  background: #16213e;
  color: #e0e0e0;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
}

.lang-btn:hover {
  background: #0f3460;
  border-color: #e94560;
}

.lang-btn.active {
  background: #e94560;
  border-color: #e94560;
  color: white;
  font-weight: 600;
}
```

---

## 5. ⚙️ Pipeline Completo em Python (Serviço Celery)

```python
# aos-domain-lms-s2st/src/workers/dubbing_worker.py

import os
import json
import tempfile
from celery import shared_task
from pathlib import Path

from ..services.asr_service import ASRService
from ..services.diarization_service import DiarizationService
from ..services.translation_service import TranslationService
from ..services.tts_service import TTSService
from ..services.sync_service import SyncService
from ..services.mux_service import MuxService
from ..services.hls_service import HLSService
from ..models.dubbing_job import DubbingJob

# Idiomas suportados para dublagem
SUPPORTED_LANGUAGES = ["en", "es", "fr", "de", "it", "zh", "ja", "ar", "ru"]

@shared_task(bind=True, max_retries=3)
def process_video_dubbing(self, video_id: str, video_path: str, source_lang: str = "pt"):
    """
    Pipeline completo de dublagem automática.
    Processa um vídeo e gera versões dubladas em múltiplos idiomas.
    """

    job = DubbingJob.create(video_id=video_id, status="processing")

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # ─── ETAPA 1: EXTRAIR ÁUDIO ──────────────────────────────
            self.update_state(state="PROGRESS", meta={"step": 1, "total": 6, "detail": "Extraindo áudio do vídeo"})

            audio_path = tmpdir / "audio.wav"
            os.system(f'ffmpeg -i "{video_path}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "{audio_path}" -y')

            # ─── ETAPA 2: ASR + DIARIZAÇÃO ───────────────────────────
            self.update_state(state="PROGRESS", meta={"step": 2, "total": 6, "detail": "Transcrevendo áudio com identificação de falantes"})

            asr_service = ASRService()
            segments = asr_service.transcribe(str(audio_path), language=source_lang)

            # Salva transcrição original
            with open(tmpdir / "transcription_original.json", "w", encoding="utf-8") as f:
                json.dump(segments, f, ensure_ascii=False, indent=2)

            # ─── ETAPA 3: TRADUÇÃO ────────────────────────────────────
            self.update_state(state="PROGRESS", meta={"step": 3, "total": 6, "detail": "Traduzindo para múltiplos idiomas"})

            translation_service = TranslationService()
            translated_segments_by_lang = {}

            for target_lang in SUPPORTED_LANGUAGES:
                if target_lang == source_lang:
                    continue

                translated = translation_service.translate_segments(segments, target_lang)
                translated_segments_by_lang[target_lang] = translated

                # Salva transcrição traduzida
                with open(tmpdir / f"transcription_{target_lang}.json", "w", encoding="utf-8") as f:
                    json.dump(translated, f, ensure_ascii=False, indent=2)

            # ─── ETAPA 4: TTS COM VOICE CLONING ──────────────────────
            self.update_state(state="PROGRESS", meta={"step": 4, "total": 6, "detail": "Sintetizando áudio traduzido com clonagem de voz"})

            # Extrai amostra da voz do professor (primeiros 10s)
            speaker_sample = tmpdir / "speaker_sample.wav"
            os.system(f'ffmpeg -i "{audio_path}" -t 10 -c copy "{speaker_sample}" -y')

            tts_service = TTSService()
            sync_service = SyncService()

            audio_files_by_lang = {source_lang: str(audio_path)}  # Áudio original

            for target_lang, translated_segments in translated_segments_by_lang.items():
                # Sintetiza áudio
                synthesized = tts_service.synthesize(
                    translated_segments,
                    speaker_sample=str(speaker_sample),
                    target_lang=target_lang,
                    output_dir=tmpdir / f"audio_{target_lang}"
                )

                # Sincroniza duração
                synchronized = sync_service.synchronize(synthesized)

                # Concatena segmentos em um único arquivo
                final_audio = tmpdir / f"audio_{target_lang}.wav"
                concat_segments(synchronized, str(final_audio))

                # Converte para AAC
                final_m4a = tmpdir / f"audio_{target_lang}.m4a"
                os.system(f'ffmpeg -i "{final_audio}" -c:a aac -b:a 128k "{final_m4a}" -y')

                audio_files_by_lang[target_lang] = str(final_m4a)

            # ─── ETAPA 5: MUX / HLS ─────────────────────────────────
            self.update_state(state="PROGRESS", meta={"step": 5, "total": 6, "detail": "Gerando stream HLS com múltiplas faixas de áudio"})

            hls_service = HLSService()
            hls_output_dir = tmpdir / "hls"
            hls_output_dir.mkdir(exist_ok=True)

            master_m3u8 = hls_service.generate(
                video_path=video_path,
                audio_files=audio_files_by_lang,
                output_dir=str(hls_output_dir),
                segment_duration=4
            )

            # ─── ETAPA 6: UPLOAD ────────────────────────────────────
            self.update_state(state="PROGRESS", meta={"step": 6, "total": 6, "detail": "Fazendo upload para CDN"})

            # Upload dos segmentos HLS para S3/MinIO
            cdn_base_url = upload_to_cdn(hls_output_dir, video_id)

            # Atualiza job
            job.update(
                status="completed",
                hls_url=f"{cdn_base_url}/master.m3u8",
                available_languages=list(audio_files_by_lang.keys()),
                transcription_original=segments,
                transcription_translated=translated_segments_by_lang
            )

            # Emite evento
            from aos_core_eventbus import AOSEventBus
            bus = AOSEventBus()
            bus.publish("lms.dubbing.completed", {
                "video_id": video_id,
                "hls_url": f"{cdn_base_url}/master.m3u8",
                "languages": list(audio_files_by_lang.keys())
            })

            return {
                "status": "success",
                "video_id": video_id,
                "hls_url": f"{cdn_base_url}/master.m3u8",
                "languages": list(audio_files_by_lang.keys())
            }

    except Exception as exc:
        job.update(status="failed", error=str(exc))
        self.retry(countdown=60, exc=exc)


def concat_segments(segments: list, output_path: str):
    """Concatena múltiplos segmentos de áudio em um único arquivo"""
    from pydub import AudioSegment

    combined = AudioSegment.empty()

    for i, seg in enumerate(segments):
        seg_audio = AudioSegment.from_wav(seg["audio_path"])

        # Adiciona silêncio se houver gap entre segmentos
        if i > 0:
            prev_end = segments[i-1]["end"]
            curr_start = seg["start"]
            gap_ms = int((curr_start - prev_end) * 1000)
            if gap_ms > 0:
                combined += AudioSegment.silent(duration=gap_ms)

        combined += seg_audio

    combined.export(output_path, format="wav")


def upload_to_cdn(hls_dir: Path, video_id: str) -> str:
    """Upload dos arquivos HLS para o CDN (S3/MinIO)"""
    import boto3

    s3 = boto3.client("s3", endpoint_url=os.getenv("S3_ENDPOINT"))
    bucket = os.getenv("S3_BUCKET", "aos-videos")

    for file_path in hls_dir.rglob("*"):
        if file_path.is_file():
            relative_path = file_path.relative_to(hls_dir)
            s3_key = f"videos/{video_id}/hls/{relative_path}"

            content_type = "application/vnd.apple.mpegurl" if file_path.suffix == ".m3u8" else "video/iso.segment"

            s3.upload_file(
                str(file_path),
                bucket,
                s3_key,
                ExtraArgs={"ContentType": content_type}
            )

    cdn_domain = os.getenv("CDN_DOMAIN", "https://cdn.aos.com")
    return f"{cdn_domain}/videos/{video_id}/hls"
```

---

## 6. 🚀 Alternativa Unificada: SeamlessM4T (Meta)

Se quiser um **modelo único** que faz tudo (speech-to-speech direto), o **SeamlessM4T** da Meta é a escolha.

### 6.1 O Que é o SeamlessM4T

O SeamlessM4T é um modelo **fundacional multilíngue e multimodal** que suporta:
- **Speech-to-Speech Translation (S2ST):** 101 idiomas de entrada → 36 idiomas de saída
- **Speech-to-Text Translation (S2TT):** 101 → 96 idiomas
- **Text-to-Speech Translation (T2ST):** 96 → 36 idiomas
- **Text-to-Text Translation (T2TT):** 96 idiomas
- **Automatic Speech Recognition (ASR):** 96 idiomas cite🛠web_search:14#3:~:text=SeamlessM4T v2...speech-to-speech translation for nearly 100 input languages and 35 (+ English) output languages cite🛠web_search:14#8:~:text=SeamlessM4T—Massively Multilingual & Multimodal Machine Translation—a single model that supports speech-to-speech translation, speech-to-text translation, text-to-speech translation, text-to-text translation, and automatic speech recognition for up to 100 languages

### 6.2 Variações do SeamlessM4T

| Modelo | Função | Latência | Uso |
|--------|--------|----------|-----|
| **SeamlessM4T v2** | Modelo base — todos os modos | Offline | Batch processing |
| **SeamlessExpressive** | Preserva expressão, tom, emoção | Offline | Dublagem profissional |
| **SeamlessStreaming** | Streaming com ~2 segundos de latência | ~2s | Ao vivo / webinars | cite🛠web_search:14#3:~:text=SeamlessStreaming...first massively multilingual model that delivers translations with around two-seconds of latency |

### 6.3 Uso no AOS

```python
from seamless_communication.streaming import StreamingTranslator

# Para processamento batch (videoaulas gravadas)
def translate_with_seamlessm4t(audio_path: str, source_lang: str, target_lang: str):
    """Traduz áudio diretamente para áudio em outro idioma"""

    translator = StreamingTranslator(
        model_name="seamlessM4T_v2_large",
        vocoder_name="vocoder_36langs",
        device="cuda"
    )

    # Carrega áudio
    audio = load_audio(audio_path, sample_rate=16000)

    # Traduz speech-to-speech
    translated_audio = translator.predict(
        input=audio,
        task="S2ST",  # Speech-to-Speech Translation
        src_lang=source_lang,  # "por" para português
        tgt_lang=target_lang,  # "eng" para inglês
    )

    return translated_audio
```

**Vantagens do SeamlessM4T:**
- **Modelo único** — não precisa de pipeline separado (ASR → NMT → TTS)
- **Preservação de prosódia** — mantém entonação, pausas, velocidade
- **Menos erros acumulados** — sem cascata de modelos

**Desvantagens:**
- Requer **mais VRAM** (~16GB para o modelo large)
- Menos controle sobre voz individual (não clona vozes específicas)
- Licença de pesquisa (não comercial sem autorização)

---

## 7. 📊 Comparativo de Abordagens

| Abordagem | Pipeline | Qualidade | Velocidade | VRAM | Controle de Voz |
|-----------|----------|-----------|------------|------|-----------------|
| **Cascata (Whisper + NLLB + XTTS)** | ASR → NMT → TTS | ⭐⭐⭐⭐ | Média | ~12GB | Total (clonagem) |
| **SeamlessM4T v2** | S2ST direto | ⭐⭐⭐⭐⭐ | Lenta | ~16GB | Limitado |
| **SeamlessStreaming** | S2ST streaming | ⭐⭐⭐⭐ | ~2s latência | ~16GB | Limitado |
| **Open-dubbing** | Pipeline pronto | ⭐⭐⭐ | Média | ~8GB | Parcial |
| **pyVideoTrans** | Pipeline completo | ⭐⭐⭐⭐ | Rápida | ~10GB | Parcial |

**Recomendação para o AOS LMS:**
- **Videoaulas gravadas:** Pipeline cascata (WhisperX + NLLB + XTTS v2) — máximo controle e qualidade
- **Webinars ao vivo:** SeamlessStreaming — latência aceitável
- **Fallback rápido:** Edge-TTS sem clonagem

---

## 8. 🗂️ Recursos Open Source

| Projeto | GitHub | Descrição |
|---------|--------|-----------|
| **WhisperX** | github.com/m-bain/whisperX | ASR + diarização + timestamps de palavra |
| **XTTS v2** | github.com/coqui-ai/TTS | Voice cloning com 6s de amostra |
| **CosyVoice** | github.com/FunAudioLLM/CosyVoice | TTS streaming com emoção |
| **NLLB-200** | github.com/facebookresearch/fairseq | Tradução 200 idiomas |
| **SeamlessM4T** | github.com/facebookresearch/seamless_communication | S2ST unificado |
| **Open-dubbing** | github.com/softcatala/open-dubbing | Pipeline de dublagem completo |
| **AutoDub** | github.com/shyhirt/AutoDub | Whisper + Ollama + XTTS offline |
| **pyVideoTrans** | github.com/jianchang512/pyvideotrans | Pipeline completo com UI |
| **Ariel (Google)** | github.com/google-marketing-solutions/ariel | Dublagem cloud-native |
| **KrillinAI** | github.com/krillinai/KrillinAI | Dublagem para shorts/reels |

---

## 9. 🎯 Conclusão

O sistema de **Speech-to-Speech Translation** do AOS LMS transforma videoaulas em **conteúdo verdadeiramente global**. Um professor angolano pode gravar uma aula em português, e alunos de todo o mundo podem assisti-la **ouvindo a própria voz do professor falando inglês, espanhol, francês ou mandarim**.

A arquitetura recomendada é:
1. **Pipeline cascata** (WhisperX → NLLB → XTTS v2) para videoaulas gravadas — máxima qualidade e controle
2. **HLS com faixas alternativas** para entrega web — compatível com todos os navegadores
3. **Processamento batch via Celery** — não bloqueia o upload do professor
4. **Player com seletor de idioma** — experiência tipo Netflix/YouTube

O resultado é um LMS onde **o idioma deixa de ser barreira**.
