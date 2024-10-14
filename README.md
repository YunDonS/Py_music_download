下面是该项目的中文 `README.md`，详细介绍如何使用和运行音乐下载器项目：

---

### `README.md` - 音乐下载器项目

---

## 项目简介

该项目旨在根据指定的歌曲名称，通过 API 下载音乐文件（MP3 格式）。项目使用 Python 的 `requests` 库进行数据获取，并通过 `pydub` 库来检查下载的 MP3 文件是否可播放。如果歌曲无法下载或无法播放，将记录在相应的日志文件中，方便后续检查。

---

### 目录

1. [环境要求](#环境要求)
2. [安装步骤](#安装步骤)
3. [运行方法](#运行方法)
4. [功能简介](#功能简介)
5. [文件结构](#文件结构)
6. [多线程下载](#多线程下载)
7. [错误处理](#错误处理)
8. [日志记录](#日志记录)
9. [FFmpeg 配置](#ffmpeg-配置)
10. [贡献指南](#贡献指南)

---

### 环境要求

- Python 3.x
- `requests` 库
- `pydub` 库
- FFmpeg（用于音频文件处理）

---

### 安装步骤

1. **克隆仓库**:
   ```bash
   git clone https://github.com/yourusername/music-downloader.git
   cd music-downloader
   ```

2. **创建虚拟环境**（推荐）:
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # 对于 Windows，使用：myenv\Scripts\activate
   ```

3. **安装所需依赖**:
   ```bash
   pip install -r requirements.txt
   ```

4. **安装 FFmpeg**:
   - **Windows**: 从 [这里](https://ffmpeg.org/download.html) 下载并安装 FFmpeg，并确保将其添加到系统 `Path` 中。
   - **macOS**: 使用 Homebrew 安装 FFmpeg：
     ```bash
     brew install ffmpeg
     ```
   - **Linux**:
     ```bash
     sudo apt install ffmpeg
     ```

5. **在代码中设置 FFmpeg 和 FFprobe 路径**:
   代码会自动检测系统中的 FFmpeg 和 FFprobe。如果没有找到，你可以手动设置路径：

   ```python
   from pydub import AudioSegment
   from pydub.utils import which
   AudioSegment.converter = which("ffmpeg")
   AudioSegment.ffprobe = which("ffprobe")
   ```

---

### 运行方法

1. **准备歌曲列表**：
   - 在项目根目录下创建一个名为 `music.txt` 的文件。
   - 在文件中每行添加一个歌曲名称。

2. **运行脚本**：
   - 在添加了 `music.txt` 后，运行 Python 脚本开始下载音乐：
   ```bash
   python main.py
   ```

---

### 功能简介

1. **下载音乐**：
   - 通过 API 获取音乐数据，并下载 MP3 文件。
   - 保存音乐文件到 `music/` 目录。

2. **检测可播放性**：
   - 下载后，使用 `pydub` 检查 MP3 文件是否可以正常播放。
   - 无法播放的文件将记录在日志中。

3. **多线程支持**：
   - 该项目支持多线程下载，提高下载效率。

4. **错误处理**：
   - 下载失败或在 API 中找不到的歌曲会记录在日志文件中。

---

### 文件结构

- `main.py`: 主程序脚本，负责处理下载和文件验证。
- `music.txt`: 包含待下载歌曲名称的文件（每行一个歌曲名称）。
- `music/`: 下载的 MP3 文件保存的目录。
- `not_found_songs.txt`: 未找到的歌曲记录日志文件。
- `unplayable_songs.txt`: 下载后无法播放的歌曲记录日志文件。

---

### 多线程下载

该项目使用 Python 的 `ThreadPoolExecutor` 进行多线程下载，以提高下载速度。可以通过调整 `max_workers` 来控制同时运行的线程数：

```python
with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(download_song, song_names)
```

根据你的系统性能和网络速度，可以增加或减少 `max_workers` 的数量。

---

### 错误处理

1. **未找到的歌曲**：
   - 如果 API 未返回有效响应，歌曲名称将被记录在 `not_found_songs.txt` 中。
  
2. **无法播放的歌曲**：
   - 如果下载的 MP3 文件损坏或无法播放，歌曲名称将记录在 `unplayable_songs.txt` 中。
   - 使用 `pydub` 检查歌曲是否可播放。

---

### 日志记录

该项目会自动生成两个日志文件：

- **`not_found_songs.txt`**: 记录在 API 中找不到的歌曲名称。
- **`unplayable_songs.txt`**: 记录下载成功但无法播放的歌曲名称。

---

### FFmpeg 配置

`pydub` 依赖 FFmpeg 处理音频文件。你需要确保系统中安装了 FFmpeg 并将其添加到系统 `Path` 中。

如果 FFmpeg 未被找到，你可以手动在代码中指定路径：

```python
from pydub import AudioSegment
from pydub.utils import which
AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")
```

---

### 贡献指南

1. Fork 仓库。
2. 为你的功能或错误修复创建一个新分支。
3. 提交代码并创建 Pull Request。

如果有任何问题或改进建议，欢迎提 Issue 或 PR！

---

### 许可证

此项目在MIT许可证下获得许可-有关详细信息，请参阅[License](./LICENSE)文件。
---

该 `README.md` 文件为用户提供了详细的项目说明和运行指南。如果需要进一步的修改或添加内容，请告诉我！
