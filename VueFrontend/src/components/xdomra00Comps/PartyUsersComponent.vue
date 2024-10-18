
<template>
    <div class="flex six userPanel">
        <div class="flex card textCenter userCard" v-for="user in users">
                <h3 class="">{{user.name}}</h3>
                <h3>
                    <span class="label"   :class="readyStates[user.ready_for_game]">
                        {{actionStates[user.ready_for_game]}}
                    </span>
                </h3>
                <!-- <img src="" style="width: 50px; height: 50px;" class="dangerous"> -->
        </div>
    </div>
</template>


<script>

    export default {
        props: ["users"], 
    
        data()
        {
            return {
                actionStates: {true: "ready", false: "preparing"},
                readyStates: {true: "success", false: "warning"},
                // users: [
                //     {
                //         name:"user#1234",
                //         state: "ready"
                //     },
                //     {
                //         name:"user#1234",
                //         state: "ready"
                //     },
                //     {
                //         name:"user#1234",
                //         state: "ready"
                //     },
                //     {
                //         name:"user#1234",
                //         state: "ready"
                //     },
                //     {
                //         name:"user#1234",
                //         state: "ready"
                //     },
                //     {
                //         name:"user#1234",
                //         state: "ready"
                //     },
                //     {
                //         name:"user#1234",
                //         state: "ready"
                //     },
                //     {
                //         name:"user#1234",
                //         state: "ready"
                //     },
                //     {
                //         name:"user#1234",
                //         state: "ready"
                //     },

                // ]
            }
        }
}

</script>


<style scoped>

.userPanel
{
    margin: 0% 0% 0% 1%;
    padding: 0% 10% 0% 0%;
    overflow-x: auto;
    flex-wrap: nowrap;
    scrollbar-width: thin;
    scrollbar-color: #52D6B5 #FCEEDF;
}

.userCard
{
    min-width: 15%;
    margin: 1% 1% 1% 1%;
}

</style>