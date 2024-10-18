

<template>
    <div class="flex three center">
        <div class="full">
            <h3 style="padding: 0;">Party code</h3>
            <h1 style="padding: 0;">{{ code }}</h1>
        </div>
        <button class="two-third greenBack">
            <h2 class="zeroPad blackColor">
                Ready
            </h2>
        </button>
    </div>
    
</template>


<script>

export default {
        props: ['code'],
    }

</script>


<style>


</style>