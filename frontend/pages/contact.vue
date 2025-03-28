<script setup>
import { ref } from 'vue';

const name = ref('');
const email = ref('');
const message = ref('');

const handleSubmit = () => {
  if (name.value && email.value && message.value) {
    console.log('Form submitted:', {
      name: name.value,
      email: email.value,
      message: message.value,
    });

    // Reset form
    name.value = '';
    email.value = '';
    message.value = '';
  }
};
</script>

<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-8 flex justify-center items-center">
    <div class="w-full max-w-6xl rounded-3xl overflow-hidden shadow-xl bg-blue-50">
      <div class="flex flex-col md:flex-row min-h-full">
        <!-- Contact Info Section -->
        <div class="hidden lg:block flex-1 bg-gradient-to-br from-teal-500 to-blue-500 p-12 text-white">
          <h2 class="text-3xl font-bold mb-8">Contact Our Staff</h2>
          <p class="mb-8 text-lg">Have questions? Reach out to our team, and we'll get back to you as soon as possible.</p>

          <div class="space-y-6">
            <div class="flex items-center space-x-4">
              <div class="bg-white/20 p-3 rounded-full">
                <Icon name="heroicons:map-pin" class="h-6 w-6" />
              </div>
              <div>
                <h4 class="font-semibold">Our Location</h4>
                <p>123 Music Avenue, Harmony City</p>
              </div>
            </div>

            <div class="flex items-center space-x-4">
              <div class="bg-white/20 p-3 rounded-full">
                <Icon name="heroicons:phone" class="h-6 w-6" />
              </div>
              <div>
                <h4 class="font-semibold">Phone Number</h4>
                <p>+1 (555) 123-4567</p>
              </div>
            </div>

            <div class="flex items-center space-x-4">
              <div class="bg-white/20 p-3 rounded-full">
                <Icon name="heroicons:envelope" class="h-6 w-6" />
              </div>
              <div>
                <h4 class="font-semibold">Email Address</h4>
                <p>hello@resonance.com</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Contact Form Section -->
        <div class="flex-1 bg-white p-8 md:p-12">
          <h2 class="text-2xl font-bold mb-6">Send us a Message</h2>

          <form class="space-y-6" @submit.prevent="handleSubmit">
            <div class="form-control w-full">
              <label class="label"><span class="label-text font-medium">Your Name</span></label>
              <input v-model="name" type="text" placeholder="Enter your name" class="input input-bordered w-full bg-gray-50" required >
            </div>

            <div class="form-control w-full">
              <label class="label"><span class="label-text font-medium">Email Address</span></label>
              <input v-model="email" type="email" placeholder="Enter your email" class="input input-bordered w-full bg-gray-50" required >
            </div>

            <div class="form-control w-full">
              <label class="label"><span class="label-text font-medium">Your Message</span></label>
              <textarea v-model="message" placeholder="Type your message here" class="textarea textarea-bordered w-full bg-gray-50 min-h-32" required/>
            </div>

            <button type="submit" class="btn bg-orange-500 hover:bg-orange-600 text-white border-none px-8">Send Message</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
