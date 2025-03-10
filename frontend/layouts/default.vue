<script>

</script>

<template>
    <div class="min-h-screen flex flex-col">
        <navbar_header />
        <main class="flex-grow">
            <slot />
        </main>
        <footer_section />
    </div>
</template>