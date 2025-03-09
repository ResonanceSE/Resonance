<script setup>
const name = ref('');
const email = ref('');
const subject = ref('');
const message = ref('');
const showLiveChat = ref(false);
const chatMessage = ref('');
const chatMessages = ref([
    { sender: 'system', text: 'Welcome to Resonance Live Chat! This is auto-reply, please wait for a moment.', time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }
]);

const handleSubmit = () => {
    if (name.value && email.value && message.value) {
        console.log('Form submitted:', { name: name.value, email: email.value, subject: subject.value, message: message.value });
        // Reset form after submission
        name.value = '';
        email.value = '';
        subject.value = '';
        message.value = '';
    }
};

const toggleLiveChat = () => {
    showLiveChat.value = !showLiveChat.value;

    // If opening chat and no user messages yet, simulate typing indicator
    if (showLiveChat.value && chatMessages.value.length === 1) {
        setTimeout(() => {
            chatMessages.value.push({
                sender: 'agent',
                text: 'Hi there! How can I help you with Resonance today?',
                time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });
        }, 1500);
    }
};

const sendChatMessage = () => {
    if (chatMessage.value.trim() === '') return;

    // Add user message
    chatMessages.value.push({
        sender: 'user',
        text: chatMessage.value,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    });

    const userMessage = chatMessage.value;
    chatMessage.value = '';

    // Simulate agent typing indicator
    setTimeout(() => {
        // Choose a response based on message content
        let response = '';
        if (userMessage.toLowerCase().includes('price') || userMessage.toLowerCase().includes('cost')) {
            response = 'Our subscription plans start at $9.99/month. Would you like me to send you our full pricing details?';
        } else if (userMessage.toLowerCase().includes('problem') || userMessage.toLowerCase().includes('issue') || userMessage.toLowerCase().includes('help')) {
            response = 'I\'m sorry to hear you\'re having trouble. Could you provide more details about the issue you\'re experiencing?';
        } else {
            response = 'Thanks for your message! This is a demo of the live chat feature. In a real implementation, this would connect to a support agent.';
        }

        chatMessages.value.push({
            sender: 'agent',
            text: response,
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        });
    }, 1500);
};
</script>

<template>
    <div class="min-h-screen bg-gray-50 p-4 md:p-8 flex justify-center items-center">
        <div class="w-full max-w-6xl rounded-3xl overflow-hidden shadow-xl bg-blue-50">
            <div class="flex flex-col md:flex-row min-h-full">
                <!-- Left side wrapper -->
                <div class="hidden lg:block flex-1">
                    <!-- Left side - Contact Info -->
                    <div class="bg-gradient-to-br from-teal-500 to-blue-500 p-8 md:p-12 text-white relative h-full">
                        <!-- Decorative shapes -->
                        <div class="absolute right-0 top-1/4 w-24 h-24 bg-teal-300 opacity-20 rounded-l-full"/>
                        <div class="absolute left-0 bottom-1/4 w-32 h-32 bg-blue-300 opacity-20 rounded-full"/>
                        <div class="absolute right-16 bottom-40 w-12 h-12 bg-orange-500 opacity-30 rotate-45"/>

                        <div class="relative z-10">
                            <h2 class="text-3xl font-bold mb-8">Get in Touch</h2>
                            <p class="mb-12 text-lg">
                                Have questions about Resonance? Want to collaborate?
                                Drop us a message and we'll get back to you soon!
                            </p>

                            <div class="space-y-6">
                                <div class="flex items-center space-x-4">
                                    <div class="bg-white/20 p-3 rounded-full">
                                        <Icon name="heroicons:map-pin" class="h-6 w-6" aria-hidden="true" />
                                    </div>
                                    <div>
                                        <h4 class="font-semibold">Our Location</h4>
                                        <p>123 Music Avenue, Harmony City</p>
                                    </div>
                                </div>

                                <div class="flex items-center space-x-4">
                                    <div class="bg-white/20 p-3 rounded-full">
                                        <Icon name="heroicons:phone" class="h-6 w-6" aria-hidden="true" />
                                    </div>
                                    <div>
                                        <h4 class="font-semibold">Phone Number</h4>
                                        <p>+1 (555) 123-4567</p>
                                    </div>
                                </div>

                                <div class="flex items-center space-x-4">
                                    <div class="bg-white/20 p-3 rounded-full">
                                        <Icon name="heroicons:envelope" class="h-6 w-6" aria-hidden="true" />
                                    </div>
                                    <div>
                                        <h4 class="font-semibold">Email Address</h4>
                                        <p>hello@resonance.com</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Right side wrapper -->
                <div class="flex-1 md:w-1/2">
                    <!-- Right side - Contact Form -->
                    <div class="bg-white p-8 md:p-12 h-full">
                        <h2 class="text-2xl font-bold mb-6">Send us a Message</h2>

                        <form class="space-y-6" @submit.prevent="handleSubmit">
                            <div class="form-control w-full">
                                <label class="label">
                                    <span class="label-text font-medium">Your Name</span>
                                </label>
                                <input
v-model="name" type="text" placeholder="Enter your name"
                                    class="input input-bordered w-full bg-gray-50" required >
                            </div>

                            <div class="form-control w-full">
                                <label class="label">
                                    <span class="label-text font-medium">Email Address</span>
                                </label>
                                <input
v-model="email" type="email" placeholder="Enter your email"
                                    class="input input-bordered w-full bg-gray-50" required >
                            </div>

                            <div class="form-control w-full">
                                <label class="label">
                                    <span class="label-text font-medium">Subject</span>
                                </label>
                                <input
v-model="subject" type="text" placeholder="What is this regarding?"
                                    class="input input-bordered w-full bg-gray-50" >
                            </div>

                            <div class="form-control w-full">
                                <label class="label">
                                    <span class="label-text font-medium">Your Message</span>
                                </label>
                                <textarea
v-model="message" placeholder="Type your message here"
                                    class="textarea textarea-bordered w-full bg-gray-50 min-h-32" required/>
                            </div>

                            <div class="flex flex-col sm:flex-row gap-4">
                                <button
type="submit"
                                    class="btn bg-orange-500 hover:bg-orange-600 text-white border-none px-8">
                                    Send Message
                                </button>

                                <button
type="button" class="btn bg-teal-500 hover:bg-teal-600 text-white border-none px-8"
                                    @click="toggleLiveChat">
                                    <Icon
v-if="!showLiveChat" name="heroicons:chat-bubble-left-right"
                                        class="h-5 w-5 mr-2" />
                                    <Icon v-else name="heroicons:x-mark" class="h-5 w-5 mr-2" />
                                    {{ showLiveChat ? 'Close Chat' : 'Start Live Chat' }}
                                </button>
                            </div>
                        </form>

                        <!-- Live Chat Modal -->
                        <input id="live-chat-modal" v-model="showLiveChat" type="checkbox" class="modal-toggle" >
                        <div class="modal" :class="{ 'modal-open': showLiveChat }">
                            <div
                                class="modal-box relative w-11/12 max-w-md md:max-w-lg bg-white p-0 rounded-lg shadow-xl">
                                <!-- Chat Header -->
                                <div class="bg-teal-500 text-white p-4 rounded-t-lg flex justify-start items-center">
                                    <div class="flex items-center">
                                        <div
                                            class="bg-white text-teal-500 rounded-full h-8 w-8 flex items-center justify-center mr-3">
                                            <Icon name="heroicons:chat-bubble-left-right" class="h-5 w-5" />
                                        </div>
                                        <span class="font-semibold">Resonance Live Support</span>
                                    </div>
                                    <div class="flex items-center">
                                        <span class="inline-block h-2 w-2 bg-green-400 rounded-full mx-2"/>
                                        <span class="text-sm text-left">Online</span>
                                    </div>
                                </div>

                                <!-- Chat Messages -->
                                <div class="bg-gray-50 h-80 p-4 overflow-y-auto">
                                    <div class="chat flex flex-col gap-3">

                                        <div v-for="(msg, index) in chatMessages" :key="index">
                                            <div
:class="[
                                                'chat-bubble max-w-xs md:max-w-sm',
                                                msg.sender === 'user' ?  'chat-bubble-warning ml-auto chat-end' :
                                                msg.sender === 'agent' ? 'chat-bubble-neutral chat-start' :
                                                                         'chat-bubble-primary chat-start'
                                            ]">
                                                {{ msg.text }}
                                            </div>
                                            <div
:class="[
                                                'text-xs text-gray-500 mt-1 mb-3',
                                                msg.sender === 'user' ? 'text-right' : 'text-left'
                                            ]">
                                                {{ msg.time }}
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Chat Input -->
                                <div class="bg-white p-4 border-t border-gray-200 rounded-b-lg">
                                    <form class="flex gap-2" @submit.prevent="sendChatMessage">
                                        <input
v-model="chatMessage" type="text" placeholder="Type your message here..."
                                            class="input input-bordered flex-grow bg-gray-50" >
                                        <button
type="submit"
                                            class="btn bg-orange-500 hover:bg-orange-600 text-white border-none">
                                            <Icon name="heroicons:paper-airplane" class="h-5 w-5" />
                                        </button>
                                    </form>
                                </div>

                                <!-- Close button -->
                                <button
                                    class="btn btn-sm btn-circle absolute top-4 right-3 bg-white rounded-full w-8 h-8 flex items-center justify-center shadow-md z-10 hover:bg-gray-100"
                                    @click="toggleLiveChat">
                                    <Icon name="heroicons:x-mark" class="h-5 w-5" />
                                </button>
                            </div>
                            <!-- Modal background for click-outside closing -->
                            <label class="modal-backdrop" @click="toggleLiveChat">Close</label>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>