<script setup>
</script>

<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-8 flex justify-center items-center">
    <div class="w-full max-w-6xl rounded-3xl overflow-hidden shadow-xl bg-blue-50">
      <div class="flex flex-col md:flex-row min-h-full">
        <!-- Contact Info Section -->
        <div class="lg:flex-1 bg-gradient-to-br from-teal-500 to-blue-500 p-12 text-white">
          <h2 class="text-3xl font-bold mb-8">Contact Our Staff</h2>
          <p class="mb-8 text-lg">Have questions? Reach out to our team, and we'll get back to you as soon as possible.</p>

          <div class="space-y-6">
            <div class="flex items-center space-x-4">
              <div class="bg-white/20 p-3 rounded-full">
                <Icon name="heroicons:map-pin" class="h-6 w-6" />
              </div>
              <div>
                <h4 class="font-semibold">Our Location</h4>
                <p> 1518 Parcharat Wong Sawang, Bang Sue, Bangkok 10800</p>
              </div>
            </div>

            <div class="flex items-center space-x-4">
              <div class="bg-white/20 p-3 rounded-full">
                <Icon name="heroicons:phone" class="h-6 w-6" />
              </div>
              <div>
                <h4 class="font-semibold">Phone Number</h4>
                <p>+66 80-372-9314</p>
              </div>
            </div>

            <div class="flex items-center space-x-4">
              <div class="bg-white/20 p-3 rounded-full">
                <Icon name="heroicons:envelope" class="h-6 w-6" />
              </div>
              <div>
                <h4 class="font-semibold">Email Address</h4>
                <p>kritsakorn224@gmail.com</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Business Hours and FAQ Section -->
        <div class="flex-1 bg-white p-8 md:p-12">
          <h2 class="text-2xl font-bold mb-6">How We Can Help</h2>
          
          <!-- Business Hours -->
          <div class="mb-8">
            <h3 class="text-lg font-semibold mb-3">Business Hours</h3>
            <div class="space-y-2">
              <div class="flex justify-between">
                <span>Monday - Friday:</span>
                <span>9:00 AM - 6:00 PM</span>
              </div>
              <div class="flex justify-between">
                <span>Saturday:</span>
                <span>10:00 AM - 4:00 PM</span>
              </div>
              <div class="flex justify-between">
                <span>Sunday:</span>
                <span>Closed</span>
              </div>
            </div>
          </div>
          
          <!-- Support Options -->
          <div class="mb-8">
            <h3 class="text-lg font-semibold mb-3">Support Options</h3>
            <div class="space-y-4">

              
              <div class="flex items-start gap-3">
                <div class="bg-orange-100 p-2 rounded-full mt-1">
                  <Icon name="heroicons:envelope" class="h-5 w-5 text-orange-500" />
                </div>
                <div>
                  <h4 class="font-medium">Email Support</h4>
                  <p class="text-sm text-gray-600">24/7 email support with a response within 24 hours</p>
                </div>
              </div>
              
              <div class="flex items-start gap-3">
                <div class="bg-orange-100 p-2 rounded-full mt-1">
                  <Icon name="heroicons:phone" class="h-5 w-5 text-orange-500" />
                </div>
                <div>
                  <h4 class="font-medium">Phone Support</h4>
                  <p class="text-sm text-gray-600">Call our team for direct assistance during business hours</p>
                </div>
              </div>
            </div>
          </div>
          
          <div class="mt-8 flex justify-center">
            <a href="mailto:kritsakorn224@gmail.com" class="btn bg-orange-500 hover:bg-orange-600 text-white border-none px-8">
              Email Us Now
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>