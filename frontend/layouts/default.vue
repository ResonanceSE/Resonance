<script>

</script>

<template>
    <div class="min-h-screen flex flex-col">
        <NavbarHeader/>
        <main class="flex-grow">
            <slot />
        </main>
        <FooterSection />
    </div>
</template>