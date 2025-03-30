<template>
  <div class="website-container">
    <!-- Website Title -->
    <div class="website-header">
      <h1 class="website-title">Chat Assistant</h1>
      <p class="website-subtitle">Giải đáp thắc mắc về quy chế học vụ Trường Đại học Cần Thơ</p>
    </div>
    
    <!-- Chat Container -->
    <div class="chat-container">
      <div class="chat-box" ref="chatBox">
        <div v-for="(message, index) in messages" 
             :key="index" 
             class="chat-message-wrapper" 
             :class="message.type">
          <img class="avatar" v-if="message.type === 'bot'" src="@/assets/bot_avt.jpg" />
          <span class="message-text">{{ message.text }}</span>
          <img class="avatar" v-if="message.type === 'user'" src="@/assets/user_avt.jpg" />
        </div>
      </div>

      <div class="chat-input">
        <input type="text"
               v-model="userInput"
               placeholder="Đặt câu hỏi..."
               @keyup.enter="sendMessage"
        />
        <button type="button" @click="sendMessage">Gửi</button>
        <button type="button" @click="clearChat" class="clear-btn">Xoá trò chuyện</button>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
export default {
  name: "Answer",
  data() {
    return {
      userInput: "",
      messages: [], // Stores chat messages
    };
  },
  mounted() {
    // Add initial bot greeting when component is mounted
    this.messages.push({
      text: "Xin chào! Tôi là trợ lý hỗ trợ quy chế học vụ Trường Đại học Cần Thơ. Bạn có thể hỏi tôi về các vấn đề liên quan đến học vụ, như đăng ký lớp học phần, điều kiện tốt nghiệp, học bổng, hay các quy định đào tạo khác. Tôi sẵn sàng giúp bạn!",
      type: "bot"
    });
  },
  methods: {
    async sendMessage() {
      if (this.userInput.trim() === "") return; // Ignore empty messages

      console.log("Sending request:", { message: this.userInput }); // Debug log
      
      // Add user's message to chat
      this.messages.push({ text: this.userInput, type: "user" });
      await this.$nextTick(); // Ensure DOM updates

      try {
        // Send user input to the backend API
        const response = await axios.post(
          "http://127.0.0.1:5000/classify", 
          { message: this.userInput },
          { headers: { "Content-Type": "application/json" } } // Explicitly set JSON headers
          
        );
        
        console.log("Received response:", response.data); // Debug log

        // Add bot's response to chat
        this.messages.push({ text: response.data.response, type: "bot" });
      } catch (error) {
        console.error("Error fetching bot response:", error);
        this.messages.push({
          text: "Có lỗi xảy ra, vui lòng thử lại",
          type: "bot",
        });
      }
      

      // Clear input field and scroll chat down
      this.userInput = "";
      this.$nextTick(() => this.scrollToBottom());
    },
    clearChat() {
      this.messages = []; // Reset chat history

      // Re-add initial greeting after clearing
      this.messages.push({
        text: "Xin chào! Tôi là trợ lý hỗ trợ quy chế học vụ Trường Đại học Cần Thơ. Bạn có thể hỏi tôi về các vấn đề liên quan đến học vụ, như đăng ký lớp học phần, điều kiện tốt nghiệp, học bổng, hay các quy định đào tạo khác!",
        type: "bot"
      });

      this.$nextTick(() => this.scrollToBottom());
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const chatBox = this.$refs.chatBox;
        if (chatBox) {
          chatBox.scrollTop = chatBox.scrollHeight;
        }
      });
    }
  }
};
</script>

<style src="@/assets/chatbot.css"></style>
<style scoped></style>
